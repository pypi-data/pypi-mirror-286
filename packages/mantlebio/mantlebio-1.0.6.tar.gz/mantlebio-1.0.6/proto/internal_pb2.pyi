from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Cron(_message.Message):
    __slots__ = ("name", "tenant", "last_run")
    NAME_FIELD_NUMBER: _ClassVar[int]
    TENANT_FIELD_NUMBER: _ClassVar[int]
    LAST_RUN_FIELD_NUMBER: _ClassVar[int]
    name: str
    tenant: str
    last_run: _timestamp_pb2.Timestamp
    def __init__(self, name: _Optional[str] = ..., tenant: _Optional[str] = ..., last_run: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class UpdateCron(_message.Message):
    __slots__ = ("last_run",)
    LAST_RUN_FIELD_NUMBER: _ClassVar[int]
    last_run: _timestamp_pb2.Timestamp
    def __init__(self, last_run: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...
