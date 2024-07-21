import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple, Union
from uuid import UUID, uuid4

import orjson
from pydantic import BaseModel, Field

MAX_LAYER_DEPTH = 2
LOGGER = logging.getLogger(__name__)


class ExtraRunData(BaseModel):
    """
    Extra fields that can be added at runtime.
    """

    tags: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None
    user_id: Optional[str] = None
    correlation_id: Optional[str] = None


class InferenceStats(BaseModel):
    inference_model: str
    inference_provider: str
    input_tokens: int
    output_tokens: int
    total_tokens: int


class Run(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    project_id: str
    name: str
    run_type: str
    start_time: datetime
    inputs: Tuple[Any, ...]
    sub_runs: List["Run"] = []
    parent_id: Optional[UUID]
    graph_id: UUID
    app_path: str
    status: str
    error: Optional[str] = None
    end_time: Optional[datetime] = None
    latency: Optional[int] = None
    outputs: Optional[Union[Any, List[Any]]] = None
    tags: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None
    user_id: Optional[str]
    correlation_id: Optional[str]
    inference_stats: Optional[List[InferenceStats]] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: str,
            Tuple: list,
            set: list,
        }

    def set_end_time_and_latency(self):
        self.end_time = datetime.now(timezone.utc)
        self.latency = round((self.end_time - self.start_time).total_seconds() * 1000)

    def complete(self):
        self.set_end_time_and_latency()
        self.status = "completed"

    def fail(self, error: Exception):
        self.set_end_time_and_latency()
        self.status = "failed"
        self.error = str(error)

    def finalize(self):
        if self.status == "running":
            self.set_end_time_and_latency()
            self.status = "canceled"

    def update_inference_stats(self, result):
        if result.usage is not None:
            inference_stats = InferenceStats(
                inference_model=result.model,
                inference_provider="",
                input_tokens=0,
                output_tokens=0,
                total_tokens=0,
            )
            if hasattr(result.usage, "input_tokens") and hasattr(
                result.usage, "output_tokens"
            ):
                inference_stats.input_tokens = result.usage.input_tokens
                inference_stats.output_tokens = result.usage.output_tokens
                inference_stats.total_tokens = (
                    inference_stats.input_tokens + inference_stats.output_tokens
                )
            if (
                hasattr(result.usage, "prompt_tokens")
                and hasattr(result.usage, "completion_tokens")
                and hasattr(result.usage, "total_tokens")
            ):
                inference_stats.input_tokens = result.usage.prompt_tokens
                inference_stats.output_tokens = result.usage.completion_tokens
                inference_stats.total_tokens = result.usage.total_tokens
            if self.inference_stats is None:
                self.inference_stats = []
            self.inference_stats.append(inference_stats)

    def update_parent_run(self, parent_run):
        if self.inference_stats is not None:
            if parent_run.inference_stats is None:
                parent_run.inference_stats = []
            parent_run.inference_stats.extend(self.inference_stats)


def serialize_run(run: Run) -> Any:
    try:
        run_dict = dict(run)
        json_str = _dumps_json(run_dict)
        json = orjson.loads(json_str)
    except Exception as e:
        LOGGER.error(f"Failed to serialize run: {e}")
        json_str = orjson.dumps(repr(run))  # todo: improve this fallback
        json = orjson.loads(json_str)

    return json


def _dumps_json(ob, layer=0):
    try:
        return orjson.dumps(
            ob,
            default=lambda o: _default_serializer(o, layer),
            option=orjson.OPT_NON_STR_KEYS | orjson.OPT_SERIALIZE_NUMPY,
        )
    except Exception as e:
        LOGGER.warning(f"Failed to serialize object: {e}")
        return orjson.dumps(repr(ob))


def _try_serialize(ob, func_attr, exclude_none, layer):
    if hasattr(ob, func_attr) and callable(getattr(ob, func_attr)):
        try:
            func = getattr(ob, func_attr)
            json_str = func(exclude_none=exclude_none) if exclude_none else func()

            if isinstance(json_str, str):
                return orjson.loads(json_str)

            return orjson.loads(_dumps_json(json_str, layer=layer + 1))
        except Exception as e:
            LOGGER.debug(f"Failed to use serialization function '{func_attr}': {e}")
    return None


def _default_serializer(ob, layer):
    if layer >= MAX_LAYER_DEPTH:
        return repr(ob)

    possible_serialization_functions = [
        {"func_attr": "model_dump_json", "exclude_none": True},
        {"func_attr": "json", "exclude_none": True},
        {"func_attr": "to_json", "exclude_none": False},
        {"func_attr": "model_dump", "exclude_none": True},
        {"func_attr": "dict", "exclude_none": False},
        {"func_attr": "to_dict", "exclude_none": False},
    ]

    for func_info in possible_serialization_functions:
        result = _try_serialize(
            ob, func_info["func_attr"], func_info["exclude_none"], layer=layer
        )
        if result is not None:
            return result

    if isinstance(ob, (set, tuple)):
        return list(ob)
    if isinstance(ob, datetime):
        return ob.isoformat()
    if isinstance(ob, UUID):
        return str(ob)
    if isinstance(ob, bytes):
        return ob.decode("utf-8")
    if hasattr(ob, "__dict__"):
        ob_dict = vars(ob)

        if not ob_dict:
            return repr(ob)

        return {k: _default_serializer(v, layer + 1) for k, v in ob_dict.items()}
    return repr(ob)
