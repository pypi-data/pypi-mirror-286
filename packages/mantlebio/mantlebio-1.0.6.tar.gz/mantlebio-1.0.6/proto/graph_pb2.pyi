from proto import entity_pb2 as _entity_pb2
from proto import analysis_pb2 as _analysis_pb2
from proto import common_pb2 as _common_pb2
from proto import pipeline_run_pb2 as _pipeline_run_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EntityRelationResponse(_message.Message):
    __slots__ = ("entity", "created_by", "used_in")
    ENTITY_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_FIELD_NUMBER: _ClassVar[int]
    USED_IN_FIELD_NUMBER: _ClassVar[int]
    entity: _entity_pb2.Entity
    created_by: EntityRelation
    used_in: _containers.RepeatedCompositeFieldContainer[EntityRelation]
    def __init__(self, entity: _Optional[_Union[_entity_pb2.Entity, _Mapping]] = ..., created_by: _Optional[_Union[EntityRelation, _Mapping]] = ..., used_in: _Optional[_Iterable[_Union[EntityRelation, _Mapping]]] = ...) -> None: ...

class EntityRelation(_message.Message):
    __slots__ = ("pipeline_run", "analysis", "user", "relation_type")
    class RelationType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        INVALID: _ClassVar[EntityRelation.RelationType]
        PARENT: _ClassVar[EntityRelation.RelationType]
        CHILD: _ClassVar[EntityRelation.RelationType]
    INVALID: EntityRelation.RelationType
    PARENT: EntityRelation.RelationType
    CHILD: EntityRelation.RelationType
    PIPELINE_RUN_FIELD_NUMBER: _ClassVar[int]
    ANALYSIS_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    RELATION_TYPE_FIELD_NUMBER: _ClassVar[int]
    pipeline_run: _pipeline_run_pb2.PipelineRun
    analysis: _analysis_pb2.Analysis
    user: _common_pb2.User
    relation_type: EntityRelation.RelationType
    def __init__(self, pipeline_run: _Optional[_Union[_pipeline_run_pb2.PipelineRun, _Mapping]] = ..., analysis: _Optional[_Union[_analysis_pb2.Analysis, _Mapping]] = ..., user: _Optional[_Union[_common_pb2.User, _Mapping]] = ..., relation_type: _Optional[_Union[EntityRelation.RelationType, str]] = ...) -> None: ...

class NodeEntity(_message.Message):
    __slots__ = ("id", "entity", "origin", "created_by_edge")
    ID_FIELD_NUMBER: _ClassVar[int]
    ENTITY_FIELD_NUMBER: _ClassVar[int]
    ORIGIN_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_EDGE_FIELD_NUMBER: _ClassVar[int]
    id: str
    entity: _entity_pb2.Entity
    origin: _entity_pb2.Origin
    created_by_edge: str
    def __init__(self, id: _Optional[str] = ..., entity: _Optional[_Union[_entity_pb2.Entity, _Mapping]] = ..., origin: _Optional[_Union[_entity_pb2.Origin, _Mapping]] = ..., created_by_edge: _Optional[str] = ...) -> None: ...

class EntityGraph(_message.Message):
    __slots__ = ("focus", "nodes", "edges")
    FOCUS_FIELD_NUMBER: _ClassVar[int]
    NODES_FIELD_NUMBER: _ClassVar[int]
    EDGES_FIELD_NUMBER: _ClassVar[int]
    focus: NodeEntity
    nodes: _containers.RepeatedCompositeFieldContainer[NodeEntity]
    edges: _containers.RepeatedCompositeFieldContainer[Edge]
    def __init__(self, focus: _Optional[_Union[NodeEntity, _Mapping]] = ..., nodes: _Optional[_Iterable[_Union[NodeEntity, _Mapping]]] = ..., edges: _Optional[_Iterable[_Union[Edge, _Mapping]]] = ...) -> None: ...

class Edge(_message.Message):
    __slots__ = ("id", "pipeline_run", "analysis", "input_entities", "output_entities")
    ID_FIELD_NUMBER: _ClassVar[int]
    PIPELINE_RUN_FIELD_NUMBER: _ClassVar[int]
    ANALYSIS_FIELD_NUMBER: _ClassVar[int]
    INPUT_ENTITIES_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_ENTITIES_FIELD_NUMBER: _ClassVar[int]
    id: str
    pipeline_run: _pipeline_run_pb2.PipelineRun
    analysis: _analysis_pb2.Analysis
    input_entities: _containers.RepeatedScalarFieldContainer[str]
    output_entities: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, id: _Optional[str] = ..., pipeline_run: _Optional[_Union[_pipeline_run_pb2.PipelineRun, _Mapping]] = ..., analysis: _Optional[_Union[_analysis_pb2.Analysis, _Mapping]] = ..., input_entities: _Optional[_Iterable[str]] = ..., output_entities: _Optional[_Iterable[str]] = ...) -> None: ...
