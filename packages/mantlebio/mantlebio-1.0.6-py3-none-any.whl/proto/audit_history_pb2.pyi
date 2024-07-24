from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AuditHistorySubject(_message.Message):
    __slots__ = ("id", "type")
    class SubjectType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        INVALID: _ClassVar[AuditHistorySubject.SubjectType]
        ENTITY: _ClassVar[AuditHistorySubject.SubjectType]
        PIPELINE_RUN: _ClassVar[AuditHistorySubject.SubjectType]
        ANALYSIS: _ClassVar[AuditHistorySubject.SubjectType]
        BENCHLING_ENTITY: _ClassVar[AuditHistorySubject.SubjectType]
        BENCHLING_PLATE: _ClassVar[AuditHistorySubject.SubjectType]
        BENCHLING_RESULT: _ClassVar[AuditHistorySubject.SubjectType]
        USER: _ClassVar[AuditHistorySubject.SubjectType]
    INVALID: AuditHistorySubject.SubjectType
    ENTITY: AuditHistorySubject.SubjectType
    PIPELINE_RUN: AuditHistorySubject.SubjectType
    ANALYSIS: AuditHistorySubject.SubjectType
    BENCHLING_ENTITY: AuditHistorySubject.SubjectType
    BENCHLING_PLATE: AuditHistorySubject.SubjectType
    BENCHLING_RESULT: AuditHistorySubject.SubjectType
    USER: AuditHistorySubject.SubjectType
    ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    id: str
    type: AuditHistorySubject.SubjectType
    def __init__(self, id: _Optional[str] = ..., type: _Optional[_Union[AuditHistorySubject.SubjectType, str]] = ...) -> None: ...

class AuditHistoryEvent(_message.Message):
    __slots__ = ("subject", "related_subject", "timestamp", "action")
    class Action(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        INVALID: _ClassVar[AuditHistoryEvent.Action]
        CREATED: _ClassVar[AuditHistoryEvent.Action]
        UPDATED: _ClassVar[AuditHistoryEvent.Action]
        CREATED_BY: _ClassVar[AuditHistoryEvent.Action]
        UPDATED_BY: _ClassVar[AuditHistoryEvent.Action]
        ARCHIVED: _ClassVar[AuditHistoryEvent.Action]
        ARCHIVED_BY: _ClassVar[AuditHistoryEvent.Action]
        INPUT_TO: _ClassVar[AuditHistoryEvent.Action]
        OUTPUT_BY: _ClassVar[AuditHistoryEvent.Action]
        KICKED_OFF: _ClassVar[AuditHistoryEvent.Action]
    INVALID: AuditHistoryEvent.Action
    CREATED: AuditHistoryEvent.Action
    UPDATED: AuditHistoryEvent.Action
    CREATED_BY: AuditHistoryEvent.Action
    UPDATED_BY: AuditHistoryEvent.Action
    ARCHIVED: AuditHistoryEvent.Action
    ARCHIVED_BY: AuditHistoryEvent.Action
    INPUT_TO: AuditHistoryEvent.Action
    OUTPUT_BY: AuditHistoryEvent.Action
    KICKED_OFF: AuditHistoryEvent.Action
    SUBJECT_FIELD_NUMBER: _ClassVar[int]
    RELATED_SUBJECT_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    subject: AuditHistorySubject
    related_subject: AuditHistorySubject
    timestamp: _timestamp_pb2.Timestamp
    action: AuditHistoryEvent.Action
    def __init__(self, subject: _Optional[_Union[AuditHistorySubject, _Mapping]] = ..., related_subject: _Optional[_Union[AuditHistorySubject, _Mapping]] = ..., timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., action: _Optional[_Union[AuditHistoryEvent.Action, str]] = ...) -> None: ...

class GetAuditHistoryResponse(_message.Message):
    __slots__ = ("events",)
    EVENTS_FIELD_NUMBER: _ClassVar[int]
    events: _containers.RepeatedCompositeFieldContainer[AuditHistoryEvent]
    def __init__(self, events: _Optional[_Iterable[_Union[AuditHistoryEvent, _Mapping]]] = ...) -> None: ...
