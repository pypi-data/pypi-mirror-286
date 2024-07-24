from google.protobuf import timestamp_pb2 as _timestamp_pb2
from proto import pipeline_pb2 as _pipeline_pb2
from proto import common_pb2 as _common_pb2
from proto import data_type_pb2 as _data_type_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PipelineRun(_message.Message):
    __slots__ = ("id", "unique_id", "pipeline_id", "name", "pipeline_version", "created_by", "updated_by", "created_at", "updated_at", "inputs", "outputs", "log_location", "status", "conclusion", "lifecycle_status")
    class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN: _ClassVar[PipelineRun.Status]
        QUEUED: _ClassVar[PipelineRun.Status]
        STARTED: _ClassVar[PipelineRun.Status]
        RUNNING: _ClassVar[PipelineRun.Status]
        COMPLETED: _ClassVar[PipelineRun.Status]
        FAILED: _ClassVar[PipelineRun.Status]
    UNKNOWN: PipelineRun.Status
    QUEUED: PipelineRun.Status
    STARTED: PipelineRun.Status
    RUNNING: PipelineRun.Status
    COMPLETED: PipelineRun.Status
    FAILED: PipelineRun.Status
    class LifecycleStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        INVALID: _ClassVar[PipelineRun.LifecycleStatus]
        ARCHIVED: _ClassVar[PipelineRun.LifecycleStatus]
        ACTIVE: _ClassVar[PipelineRun.LifecycleStatus]
    INVALID: PipelineRun.LifecycleStatus
    ARCHIVED: PipelineRun.LifecycleStatus
    ACTIVE: PipelineRun.LifecycleStatus
    ID_FIELD_NUMBER: _ClassVar[int]
    UNIQUE_ID_FIELD_NUMBER: _ClassVar[int]
    PIPELINE_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PIPELINE_VERSION_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_FIELD_NUMBER: _ClassVar[int]
    UPDATED_BY_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    INPUTS_FIELD_NUMBER: _ClassVar[int]
    OUTPUTS_FIELD_NUMBER: _ClassVar[int]
    LOG_LOCATION_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    CONCLUSION_FIELD_NUMBER: _ClassVar[int]
    LIFECYCLE_STATUS_FIELD_NUMBER: _ClassVar[int]
    id: str
    unique_id: str
    pipeline_id: str
    name: str
    pipeline_version: str
    created_by: _common_pb2.User
    updated_by: _common_pb2.User
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    inputs: PipelineInputs
    outputs: PipelineOutputs
    log_location: _data_type_pb2.S3File
    status: PipelineRun.Status
    conclusion: str
    lifecycle_status: PipelineRun.LifecycleStatus
    def __init__(self, id: _Optional[str] = ..., unique_id: _Optional[str] = ..., pipeline_id: _Optional[str] = ..., name: _Optional[str] = ..., pipeline_version: _Optional[str] = ..., created_by: _Optional[_Union[_common_pb2.User, _Mapping]] = ..., updated_by: _Optional[_Union[_common_pb2.User, _Mapping]] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., inputs: _Optional[_Union[PipelineInputs, _Mapping]] = ..., outputs: _Optional[_Union[PipelineOutputs, _Mapping]] = ..., log_location: _Optional[_Union[_data_type_pb2.S3File, _Mapping]] = ..., status: _Optional[_Union[PipelineRun.Status, str]] = ..., conclusion: _Optional[str] = ..., lifecycle_status: _Optional[_Union[PipelineRun.LifecycleStatus, str]] = ...) -> None: ...

class PipelineInputs(_message.Message):
    __slots__ = ("data",)
    class DataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _pipeline_pb2.PipelineRunValue
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_pipeline_pb2.PipelineRunValue, _Mapping]] = ...) -> None: ...
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: _containers.MessageMap[str, _pipeline_pb2.PipelineRunValue]
    def __init__(self, data: _Optional[_Mapping[str, _pipeline_pb2.PipelineRunValue]] = ...) -> None: ...

class PipelineOutputs(_message.Message):
    __slots__ = ("data",)
    class DataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _pipeline_pb2.PipelineRunValue
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_pipeline_pb2.PipelineRunValue, _Mapping]] = ...) -> None: ...
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: _containers.MessageMap[str, _pipeline_pb2.PipelineRunValue]
    def __init__(self, data: _Optional[_Mapping[str, _pipeline_pb2.PipelineRunValue]] = ...) -> None: ...

class PipelineKickOff(_message.Message):
    __slots__ = ("pipeline_id", "pipeline_version", "name", "inputs", "external")
    PIPELINE_ID_FIELD_NUMBER: _ClassVar[int]
    PIPELINE_VERSION_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    INPUTS_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_FIELD_NUMBER: _ClassVar[int]
    pipeline_id: str
    pipeline_version: str
    name: str
    inputs: PipelineInputs
    external: bool
    def __init__(self, pipeline_id: _Optional[str] = ..., pipeline_version: _Optional[str] = ..., name: _Optional[str] = ..., inputs: _Optional[_Union[PipelineInputs, _Mapping]] = ..., external: bool = ...) -> None: ...

class PipelineStatusUpdateRequest(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: PipelineRun.Status
    def __init__(self, status: _Optional[_Union[PipelineRun.Status, str]] = ...) -> None: ...

class PipelineConclusionUpdateRequest(_message.Message):
    __slots__ = ("conclusion",)
    CONCLUSION_FIELD_NUMBER: _ClassVar[int]
    conclusion: str
    def __init__(self, conclusion: _Optional[str] = ...) -> None: ...

class PipelineLifecycleStatusUpdateRequest(_message.Message):
    __slots__ = ("lifecycle_status",)
    LIFECYCLE_STATUS_FIELD_NUMBER: _ClassVar[int]
    lifecycle_status: PipelineRun.LifecycleStatus
    def __init__(self, lifecycle_status: _Optional[_Union[PipelineRun.LifecycleStatus, str]] = ...) -> None: ...

class PutPipelineLogRequest(_message.Message):
    __slots__ = ("log_location",)
    LOG_LOCATION_FIELD_NUMBER: _ClassVar[int]
    log_location: _data_type_pb2.S3File
    def __init__(self, log_location: _Optional[_Union[_data_type_pb2.S3File, _Mapping]] = ...) -> None: ...

class PutPipelineLogRequestResponse(_message.Message):
    __slots__ = ("id", "log_location")
    ID_FIELD_NUMBER: _ClassVar[int]
    LOG_LOCATION_FIELD_NUMBER: _ClassVar[int]
    id: str
    log_location: _data_type_pb2.S3File
    def __init__(self, id: _Optional[str] = ..., log_location: _Optional[_Union[_data_type_pb2.S3File, _Mapping]] = ...) -> None: ...

class PipelineRunMetrics(_message.Message):
    __slots__ = ("completed", "failed", "running", "queued")
    COMPLETED_FIELD_NUMBER: _ClassVar[int]
    FAILED_FIELD_NUMBER: _ClassVar[int]
    RUNNING_FIELD_NUMBER: _ClassVar[int]
    QUEUED_FIELD_NUMBER: _ClassVar[int]
    completed: int
    failed: int
    running: int
    queued: int
    def __init__(self, completed: _Optional[int] = ..., failed: _Optional[int] = ..., running: _Optional[int] = ..., queued: _Optional[int] = ...) -> None: ...

class PipelineRunListResponse(_message.Message):
    __slots__ = ("pipelineRuns",)
    PIPELINERUNS_FIELD_NUMBER: _ClassVar[int]
    pipelineRuns: _containers.RepeatedCompositeFieldContainer[PipelineRun]
    def __init__(self, pipelineRuns: _Optional[_Iterable[_Union[PipelineRun, _Mapping]]] = ...) -> None: ...
