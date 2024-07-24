from google.protobuf import timestamp_pb2 as _timestamp_pb2
from proto import common_pb2 as _common_pb2
from proto import data_type_pb2 as _data_type_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class OriginSystem(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    INVALID_ORIGIN_SYSTEM: _ClassVar[OriginSystem]
    MANTLE_PIPELINE: _ClassVar[OriginSystem]
    MANTLE_ANALYSIS: _ClassVar[OriginSystem]
    MANTLE_USER: _ClassVar[OriginSystem]
    BENCHLING: _ClassVar[OriginSystem]
    INSTRUMENT: _ClassVar[OriginSystem]

class EntityIntegrationType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    INVALID_INTEGRATION: _ClassVar[EntityIntegrationType]
    BENCHLING_ENTITY: _ClassVar[EntityIntegrationType]
    BENCHLING_RESULT: _ClassVar[EntityIntegrationType]
    BENCHLING_PLATE: _ClassVar[EntityIntegrationType]

class EntityIntegrationAction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    INVALID: _ClassVar[EntityIntegrationAction]
    ARCHIVED: _ClassVar[EntityIntegrationAction]
    UPDATED: _ClassVar[EntityIntegrationAction]
    CREATED: _ClassVar[EntityIntegrationAction]

class EntityIntegrationStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    STATUS_INVALID: _ClassVar[EntityIntegrationStatus]
    STATUS_ARCHIVED: _ClassVar[EntityIntegrationStatus]
    STATUS_ACTIVE: _ClassVar[EntityIntegrationStatus]
INVALID_ORIGIN_SYSTEM: OriginSystem
MANTLE_PIPELINE: OriginSystem
MANTLE_ANALYSIS: OriginSystem
MANTLE_USER: OriginSystem
BENCHLING: OriginSystem
INSTRUMENT: OriginSystem
INVALID_INTEGRATION: EntityIntegrationType
BENCHLING_ENTITY: EntityIntegrationType
BENCHLING_RESULT: EntityIntegrationType
BENCHLING_PLATE: EntityIntegrationType
INVALID: EntityIntegrationAction
ARCHIVED: EntityIntegrationAction
UPDATED: EntityIntegrationAction
CREATED: EntityIntegrationAction
STATUS_INVALID: EntityIntegrationStatus
STATUS_ARCHIVED: EntityIntegrationStatus
STATUS_ACTIVE: EntityIntegrationStatus

class Origin(_message.Message):
    __slots__ = ("system", "id", "timestamp", "label")
    SYSTEM_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    system: OriginSystem
    id: str
    timestamp: _timestamp_pb2.Timestamp
    label: str
    def __init__(self, system: _Optional[_Union[OriginSystem, str]] = ..., id: _Optional[str] = ..., timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., label: _Optional[str] = ...) -> None: ...

class EntityList(_message.Message):
    __slots__ = ("entities",)
    ENTITIES_FIELD_NUMBER: _ClassVar[int]
    entities: _containers.RepeatedCompositeFieldContainer[Entity]
    def __init__(self, entities: _Optional[_Iterable[_Union[Entity, _Mapping]]] = ...) -> None: ...

class Entity(_message.Message):
    __slots__ = ("id", "unique_id", "version_id", "name", "data_type", "data_types", "created_at", "updated_at", "created_by", "updated_by", "origin", "properties", "props")
    class PropsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: EntityDataValue
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[EntityDataValue, _Mapping]] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    UNIQUE_ID_FIELD_NUMBER: _ClassVar[int]
    VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DATA_TYPE_FIELD_NUMBER: _ClassVar[int]
    DATA_TYPES_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_FIELD_NUMBER: _ClassVar[int]
    UPDATED_BY_FIELD_NUMBER: _ClassVar[int]
    ORIGIN_FIELD_NUMBER: _ClassVar[int]
    PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    PROPS_FIELD_NUMBER: _ClassVar[int]
    id: str
    unique_id: str
    version_id: str
    name: str
    data_type: _data_type_pb2.DataType
    data_types: _containers.RepeatedCompositeFieldContainer[_data_type_pb2.DataType]
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    created_by: _common_pb2.User
    updated_by: _common_pb2.User
    origin: Origin
    properties: EntityProperties
    props: _containers.MessageMap[str, EntityDataValue]
    def __init__(self, id: _Optional[str] = ..., unique_id: _Optional[str] = ..., version_id: _Optional[str] = ..., name: _Optional[str] = ..., data_type: _Optional[_Union[_data_type_pb2.DataType, _Mapping]] = ..., data_types: _Optional[_Iterable[_Union[_data_type_pb2.DataType, _Mapping]]] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., created_by: _Optional[_Union[_common_pb2.User, _Mapping]] = ..., updated_by: _Optional[_Union[_common_pb2.User, _Mapping]] = ..., origin: _Optional[_Union[Origin, _Mapping]] = ..., properties: _Optional[_Union[EntityProperties, _Mapping]] = ..., props: _Optional[_Mapping[str, EntityDataValue]] = ...) -> None: ...

class CreateEntityDataValue(_message.Message):
    __slots__ = ("string", "int", "double", "boolean", "s3_file", "entity", "file_upload", "list", "object")
    class List(_message.Message):
        __slots__ = ("values",)
        VALUES_FIELD_NUMBER: _ClassVar[int]
        values: _containers.RepeatedCompositeFieldContainer[CreateEntityDataValue]
        def __init__(self, values: _Optional[_Iterable[_Union[CreateEntityDataValue, _Mapping]]] = ...) -> None: ...
    class DataObject(_message.Message):
        __slots__ = ("values",)
        class ValuesEntry(_message.Message):
            __slots__ = ("key", "value")
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: CreateEntityDataValue
            def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[CreateEntityDataValue, _Mapping]] = ...) -> None: ...
        VALUES_FIELD_NUMBER: _ClassVar[int]
        values: _containers.MessageMap[str, CreateEntityDataValue]
        def __init__(self, values: _Optional[_Mapping[str, CreateEntityDataValue]] = ...) -> None: ...
    STRING_FIELD_NUMBER: _ClassVar[int]
    INT_FIELD_NUMBER: _ClassVar[int]
    DOUBLE_FIELD_NUMBER: _ClassVar[int]
    BOOLEAN_FIELD_NUMBER: _ClassVar[int]
    S3_FILE_FIELD_NUMBER: _ClassVar[int]
    ENTITY_FIELD_NUMBER: _ClassVar[int]
    FILE_UPLOAD_FIELD_NUMBER: _ClassVar[int]
    LIST_FIELD_NUMBER: _ClassVar[int]
    OBJECT_FIELD_NUMBER: _ClassVar[int]
    string: str
    int: int
    double: float
    boolean: bool
    s3_file: _data_type_pb2.S3File
    entity: Entity
    file_upload: _data_type_pb2.FileUpload
    list: CreateEntityDataValue.List
    object: CreateEntityDataValue.DataObject
    def __init__(self, string: _Optional[str] = ..., int: _Optional[int] = ..., double: _Optional[float] = ..., boolean: bool = ..., s3_file: _Optional[_Union[_data_type_pb2.S3File, _Mapping]] = ..., entity: _Optional[_Union[Entity, _Mapping]] = ..., file_upload: _Optional[_Union[_data_type_pb2.FileUpload, _Mapping]] = ..., list: _Optional[_Union[CreateEntityDataValue.List, _Mapping]] = ..., object: _Optional[_Union[CreateEntityDataValue.DataObject, _Mapping]] = ...) -> None: ...

class EntityDataValue(_message.Message):
    __slots__ = ("string", "int", "double", "boolean", "s3_file", "entity", "file_upload", "list", "object")
    class List(_message.Message):
        __slots__ = ("values",)
        VALUES_FIELD_NUMBER: _ClassVar[int]
        values: _containers.RepeatedCompositeFieldContainer[EntityDataValue]
        def __init__(self, values: _Optional[_Iterable[_Union[EntityDataValue, _Mapping]]] = ...) -> None: ...
    class DataObject(_message.Message):
        __slots__ = ("values",)
        class ValuesEntry(_message.Message):
            __slots__ = ("key", "value")
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: EntityDataValue
            def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[EntityDataValue, _Mapping]] = ...) -> None: ...
        VALUES_FIELD_NUMBER: _ClassVar[int]
        values: _containers.MessageMap[str, EntityDataValue]
        def __init__(self, values: _Optional[_Mapping[str, EntityDataValue]] = ...) -> None: ...
    STRING_FIELD_NUMBER: _ClassVar[int]
    INT_FIELD_NUMBER: _ClassVar[int]
    DOUBLE_FIELD_NUMBER: _ClassVar[int]
    BOOLEAN_FIELD_NUMBER: _ClassVar[int]
    S3_FILE_FIELD_NUMBER: _ClassVar[int]
    ENTITY_FIELD_NUMBER: _ClassVar[int]
    FILE_UPLOAD_FIELD_NUMBER: _ClassVar[int]
    LIST_FIELD_NUMBER: _ClassVar[int]
    OBJECT_FIELD_NUMBER: _ClassVar[int]
    string: str
    int: int
    double: float
    boolean: bool
    s3_file: _data_type_pb2.S3File
    entity: Entity
    file_upload: _data_type_pb2.FileUpload
    list: EntityDataValue.List
    object: EntityDataValue.DataObject
    def __init__(self, string: _Optional[str] = ..., int: _Optional[int] = ..., double: _Optional[float] = ..., boolean: bool = ..., s3_file: _Optional[_Union[_data_type_pb2.S3File, _Mapping]] = ..., entity: _Optional[_Union[Entity, _Mapping]] = ..., file_upload: _Optional[_Union[_data_type_pb2.FileUpload, _Mapping]] = ..., list: _Optional[_Union[EntityDataValue.List, _Mapping]] = ..., object: _Optional[_Union[EntityDataValue.DataObject, _Mapping]] = ...) -> None: ...

class EntityProperties(_message.Message):
    __slots__ = ("data",)
    class DataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: EntityDataValue
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[EntityDataValue, _Mapping]] = ...) -> None: ...
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: _containers.MessageMap[str, EntityDataValue]
    def __init__(self, data: _Optional[_Mapping[str, EntityDataValue]] = ...) -> None: ...

class CreatEntityRequest(_message.Message):
    __slots__ = ("name", "data_type_id", "origin", "properties", "props")
    class PropsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: CreateEntityDataValue
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[CreateEntityDataValue, _Mapping]] = ...) -> None: ...
    NAME_FIELD_NUMBER: _ClassVar[int]
    DATA_TYPE_ID_FIELD_NUMBER: _ClassVar[int]
    ORIGIN_FIELD_NUMBER: _ClassVar[int]
    PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    PROPS_FIELD_NUMBER: _ClassVar[int]
    name: str
    data_type_id: str
    origin: Origin
    properties: EntityProperties
    props: _containers.MessageMap[str, CreateEntityDataValue]
    def __init__(self, name: _Optional[str] = ..., data_type_id: _Optional[str] = ..., origin: _Optional[_Union[Origin, _Mapping]] = ..., properties: _Optional[_Union[EntityProperties, _Mapping]] = ..., props: _Optional[_Mapping[str, CreateEntityDataValue]] = ...) -> None: ...

class UpdateEntityRequest(_message.Message):
    __slots__ = ("name", "properties", "props")
    class PropsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: CreateEntityDataValue
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[CreateEntityDataValue, _Mapping]] = ...) -> None: ...
    NAME_FIELD_NUMBER: _ClassVar[int]
    PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    PROPS_FIELD_NUMBER: _ClassVar[int]
    name: str
    properties: EntityProperties
    props: _containers.MessageMap[str, CreateEntityDataValue]
    def __init__(self, name: _Optional[str] = ..., properties: _Optional[_Union[EntityProperties, _Mapping]] = ..., props: _Optional[_Mapping[str, CreateEntityDataValue]] = ...) -> None: ...

class EntityResponse(_message.Message):
    __slots__ = ("entity",)
    ENTITY_FIELD_NUMBER: _ClassVar[int]
    entity: Entity
    def __init__(self, entity: _Optional[_Union[Entity, _Mapping]] = ...) -> None: ...

class EntitiesResponse(_message.Message):
    __slots__ = ("entities", "next_page_token")
    ENTITIES_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    entities: _containers.RepeatedCompositeFieldContainer[Entity]
    next_page_token: str
    def __init__(self, entities: _Optional[_Iterable[_Union[Entity, _Mapping]]] = ..., next_page_token: _Optional[str] = ...) -> None: ...

class EntitySyncRequest(_message.Message):
    __slots__ = ("entity_id", "data_type_id")
    ENTITY_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_TYPE_ID_FIELD_NUMBER: _ClassVar[int]
    entity_id: str
    data_type_id: str
    def __init__(self, entity_id: _Optional[str] = ..., data_type_id: _Optional[str] = ...) -> None: ...

class CreateEntityIntegrationRequest(_message.Message):
    __slots__ = ("entity_integration_type", "external_id", "external_id_name", "action", "data_id")
    ENTITY_INTEGRATION_TYPE_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ID_NAME_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    DATA_ID_FIELD_NUMBER: _ClassVar[int]
    entity_integration_type: EntityIntegrationType
    external_id: str
    external_id_name: str
    action: EntityIntegrationAction
    data_id: str
    def __init__(self, entity_integration_type: _Optional[_Union[EntityIntegrationType, str]] = ..., external_id: _Optional[str] = ..., external_id_name: _Optional[str] = ..., action: _Optional[_Union[EntityIntegrationAction, str]] = ..., data_id: _Optional[str] = ...) -> None: ...

class EntityIntegrationResponse(_message.Message):
    __slots__ = ("entity_integration_id",)
    ENTITY_INTEGRATION_ID_FIELD_NUMBER: _ClassVar[int]
    entity_integration_id: str
    def __init__(self, entity_integration_id: _Optional[str] = ...) -> None: ...

class EntityIntegration(_message.Message):
    __slots__ = ("entity_id", "integration_type", "integration_status", "external_id", "created_at", "data_id", "external_id_name")
    ENTITY_ID_FIELD_NUMBER: _ClassVar[int]
    INTEGRATION_TYPE_FIELD_NUMBER: _ClassVar[int]
    INTEGRATION_STATUS_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    DATA_ID_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ID_NAME_FIELD_NUMBER: _ClassVar[int]
    entity_id: str
    integration_type: EntityIntegrationType
    integration_status: EntityIntegrationStatus
    external_id: str
    created_at: _timestamp_pb2.Timestamp
    data_id: str
    external_id_name: str
    def __init__(self, entity_id: _Optional[str] = ..., integration_type: _Optional[_Union[EntityIntegrationType, str]] = ..., integration_status: _Optional[_Union[EntityIntegrationStatus, str]] = ..., external_id: _Optional[str] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., data_id: _Optional[str] = ..., external_id_name: _Optional[str] = ...) -> None: ...

class EntityIntegrationsResponse(_message.Message):
    __slots__ = ("integrations",)
    INTEGRATIONS_FIELD_NUMBER: _ClassVar[int]
    integrations: _containers.RepeatedCompositeFieldContainer[EntityIntegration]
    def __init__(self, integrations: _Optional[_Iterable[_Union[EntityIntegration, _Mapping]]] = ...) -> None: ...

class EntityResyncData(_message.Message):
    __slots__ = ("entity_integration_type", "external_id_to_archive", "external_id_to_create", "row_identifier", "name")
    ENTITY_INTEGRATION_TYPE_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ID_TO_ARCHIVE_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ID_TO_CREATE_FIELD_NUMBER: _ClassVar[int]
    ROW_IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    entity_integration_type: EntityIntegrationType
    external_id_to_archive: str
    external_id_to_create: str
    row_identifier: str
    name: str
    def __init__(self, entity_integration_type: _Optional[_Union[EntityIntegrationType, str]] = ..., external_id_to_archive: _Optional[str] = ..., external_id_to_create: _Optional[str] = ..., row_identifier: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class EntityResyncResponseData(_message.Message):
    __slots__ = ("entity_integration_type", "archived_external_id", "archived_entity_integration_id", "created_external_id", "created_entity_integration_id")
    ENTITY_INTEGRATION_TYPE_FIELD_NUMBER: _ClassVar[int]
    ARCHIVED_EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    ARCHIVED_ENTITY_INTEGRATION_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_ENTITY_INTEGRATION_ID_FIELD_NUMBER: _ClassVar[int]
    entity_integration_type: EntityIntegrationType
    archived_external_id: str
    archived_entity_integration_id: str
    created_external_id: str
    created_entity_integration_id: str
    def __init__(self, entity_integration_type: _Optional[_Union[EntityIntegrationType, str]] = ..., archived_external_id: _Optional[str] = ..., archived_entity_integration_id: _Optional[str] = ..., created_external_id: _Optional[str] = ..., created_entity_integration_id: _Optional[str] = ...) -> None: ...

class EntityResyncRequest(_message.Message):
    __slots__ = ("resync_data",)
    RESYNC_DATA_FIELD_NUMBER: _ClassVar[int]
    resync_data: _containers.RepeatedCompositeFieldContainer[EntityResyncData]
    def __init__(self, resync_data: _Optional[_Iterable[_Union[EntityResyncData, _Mapping]]] = ...) -> None: ...

class EntityResyncResponse(_message.Message):
    __slots__ = ("resync_response_data",)
    RESYNC_RESPONSE_DATA_FIELD_NUMBER: _ClassVar[int]
    resync_response_data: _containers.RepeatedCompositeFieldContainer[EntityResyncResponseData]
    def __init__(self, resync_response_data: _Optional[_Iterable[_Union[EntityResyncResponseData, _Mapping]]] = ...) -> None: ...

class CountEntitiesResponse(_message.Message):
    __slots__ = ("count",)
    COUNT_FIELD_NUMBER: _ClassVar[int]
    count: int
    def __init__(self, count: _Optional[int] = ...) -> None: ...
