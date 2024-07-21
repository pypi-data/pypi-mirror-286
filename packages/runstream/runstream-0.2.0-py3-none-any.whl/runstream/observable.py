import contextlib
import contextvars
import functools
import inspect
import os
from datetime import datetime, timezone
from typing import Any, Callable, Optional, Union
from uuid import uuid4

from runstream.api import Client
from runstream.model import ExtraRunData, Run

# todo:
# - create/cleanup api session for each top-level run

RUNSTREAM_PROJECT_ID = os.getenv("RUNSTREAM_PROJECT_ID")

client_var = contextvars.ContextVar[Optional[Client]]("client", default=None)
parent_run_var = contextvars.ContextVar[Optional[Run]]("parent_run", default=None)
extra_data_var = contextvars.ContextVar[Optional[ExtraRunData]](
    "extra_data", default=None
)


def get_run_type(func):
    if inspect.isasyncgenfunction(func):
        return "async_generator"
    elif inspect.isgeneratorfunction(func):
        return "generator"
    elif inspect.iscoroutinefunction(func):
        return "async_function"
    else:
        return "sync_function"


@contextlib.contextmanager
def run_context(func, args, extra_data: Optional[ExtraRunData], kwargs):
    function_name = func.__name__
    client = client_var.get(None)
    parent_run = parent_run_var.get(None)
    graph_id = parent_run.graph_id if parent_run else uuid4()
    run_type = get_run_type(func)

    if not client:
        client = Client()
        client_var.set(client)

    try:
        app_path = inspect.getfile(func)
    except Exception:
        app_path = ""

    # use extra_data if provided, otherwise use parent's extra_data
    parent_extra_data = extra_data_var.get(None)
    extra_data = extra_data or parent_extra_data

    if extra_data:
        extra_data_var.set(extra_data)
        user_id = extra_data.user_id
        correlation_id = extra_data.correlation_id
        tags = extra_data.tags
        metadata = extra_data.metadata
    else:
        user_id, correlation_id, tags, metadata = None, None, [], None

    run = Run(
        id=uuid4(),
        project_id=RUNSTREAM_PROJECT_ID,
        name=function_name,
        run_type=run_type,
        start_time=datetime.now(timezone.utc),
        inputs=(args, kwargs),
        sub_runs=[],
        parent_id=parent_run.id if parent_run else None,
        graph_id=graph_id,
        app_path=app_path,
        status="running",
        user_id=user_id,
        correlation_id=correlation_id,
        tags=tags,
        metadata=metadata,
    )

    if parent_run:
        parent_run.sub_runs.append(run)

    client.submit_run(run)
    parent_run_var.set(run)

    try:
        yield run
        run.complete()
    except Exception as e:
        run.fail(e)
        raise
    finally:
        if parent_run:
            run.update_parent_run(parent_run)
        run.finalize()
        parent_run_var.set(parent_run)
        client.submit_run(run)


def observable(
    *args: Any,
    **kwargs: Any,
) -> Union[Callable, Callable[[Callable], Callable]]:
    """This decorator makes a function observable in Runstream.

    Args:
        observable_type: This sets the type of the observable.
            Examples: "function", "llm", etc. Defaults to "function".
    """
    observable_type = kwargs.pop("observable_type", "function")

    def decorator(func: Callable):
        @functools.wraps(func)
        async def async_gen_wrapper(
            *args, extra_data: Optional[ExtraRunData] = None, **kwargs
        ):
            with run_context(func, args, extra_data, kwargs) as run:
                result_list = []
                async for item in func(*args, **kwargs):
                    result_list.append(item)
                    yield item
                run.outputs = result_list

        @functools.wraps(func)
        def gen_wrapper(*args, extra_data: Optional[ExtraRunData] = None, **kwargs):
            with run_context(func, args, extra_data, kwargs) as run:
                result_list = []
                for item in func(*args, **kwargs):
                    result_list.append(item)
                    yield item
                run.outputs = result_list

        @functools.wraps(func)
        async def async_wrapper(
            *args, extra_data: Optional[ExtraRunData] = None, **kwargs
        ):
            with run_context(func, args, extra_data, kwargs) as run:
                result = await func(*args, **kwargs)
                run.outputs = result
                return result

        @functools.wraps(func)
        def wrapper(*args, extra_data: Optional[ExtraRunData] = None, **kwargs):
            with run_context(func, args, extra_data, kwargs) as run:
                result = func(*args, **kwargs)
                run.outputs = result
                # todo: organize this a bit more
                if observable_type == "llm":
                    run.update_inference_stats(result)
                return result

        if inspect.isasyncgenfunction(func):
            return async_gen_wrapper
        elif inspect.isgeneratorfunction(func):
            return gen_wrapper
        elif inspect.iscoroutinefunction(func):
            return async_wrapper
        else:
            return wrapper

    if len(args) == 1 and callable(args[0]) and not kwargs:
        return decorator(args[0])
    else:
        return decorator
