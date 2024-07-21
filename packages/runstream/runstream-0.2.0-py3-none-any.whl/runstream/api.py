import atexit
import logging
import os
import queue
import threading

import requests

from runstream.model import Run, serialize_run

RUNSTREAM_API_KEY = os.getenv("RUNSTREAM_API_KEY")
RUNSTREAM_URL = os.getenv("RUNSTREAM_URL", "https://runstream.dev")
LOGGER = logging.getLogger(__name__)


class Client:
    _instance = None
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._instance_lock:
                if cls._instance is None:
                    cls._instance = super(Client, cls).__new__(cls)
                    cls._instance._init_once(*args, **kwargs)
        return cls._instance

    def _init_once(self, num_threads=3):
        self.task_queue = queue.Queue()
        self.threads = []
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Content-Type": "application/json",
                "X-API-KEY": RUNSTREAM_API_KEY,
            }
        )
        self.shutdown_event = threading.Event()
        for _ in range(num_threads):
            t = threading.Thread(target=self._process_queue)
            t.start()
            self.threads.append(t)

        atexit.register(self.close)

    def submit_run(self, run: Run):
        self.task_queue.put(run)

    def _process_queue(self):
        while not self.shutdown_event.is_set() or not self.task_queue.empty():
            try:
                run = self.task_queue.get(timeout=1)
                self._post_run(run)
                self.task_queue.task_done()
            except queue.Empty:
                continue

    def _post_run(self, run: Run):
        run_json = serialize_run(run)
        response = self.session.post(f"{RUNSTREAM_URL}/api/runs", json=run_json)
        if response.status_code != 200:
            LOGGER.error(f"Failed to post run: {response.content}")

    def close(self):
        self.shutdown_event.set()

        self.task_queue.join()

        for t in self.threads:
            t.join()

        self.session.close()
        LOGGER.debug("Runstream client closed")
