import os

from runstream.observable import observable


class MessagesProxy:
    def __init__(self, messages):
        self._messages = messages
        self.create = observable(messages.create, observable_type="llm")
        # todo: self.acreate = observable(messages.acreate, observable_type="llm")

    def __getattr__(self, name):
        return getattr(self._messages, name)


class RunstreamClient:
    def __init__(self, client):
        if (
            os.getenv("RUNSTREAM_PROJECT_ID") is None
            or os.getenv("RUNSTREAM_API_KEY") is None
        ):
            raise ValueError("Project ID and API Key are required")

        self.client = client
        self.messages = MessagesProxy(self.client.messages)

    @staticmethod
    def enable(client):
        return RunstreamClient(client)
