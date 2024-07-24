from google.protobuf import timestamp_pb2 as _timestamp_pb2
from proto import data_type_pb2 as _data_type_pb2
from proto import entity_pb2 as _entity_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PipelineOptionAction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CREATE: _ClassVar[PipelineOptionAction]
    ARCHIVE: _ClassVar[PipelineOptionAction]
    UNARCHIVE: _ClassVar[PipelineOptionAction]
CREATE: PipelineOptionAction
ARCHIVE: PipelineOptionAction
UNARCHIVE: PipelineOptionAction

class PipelineList(_message.Message):
    __slots__ = ("pipelines",)
    PIPELINES_FIELD_NUMBER: _ClassVar[int]
    pipelines: _containers.RepeatedCompositeFieldContainer[Pipeline]
    def __init__(self, pipelines: _Optional[_Iterable[_Union[Pipeline, _Mapping]]] = ...) -> None: ...

class PipelineInputConfig(_message.Message):
    __slots__ = ("type", "allow_multiple", "required")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    ALLOW_MULTIPLE_FIELD_NUMBER: _ClassVar[int]
    REQUIRED_FIELD_NUMBER: _ClassVar[int]
    type: str
    allow_multiple: bool
    required: bool
    def __init__(self, type: _Optional[str] = ..., allow_multiple: bool = ..., required: bool = ...) -> None: ...

class Pipeline(_message.Message):
    __slots__ = ("id", "name", "description", "created_at", "version", "version_number", "batch_queue_arn", "entry", "inputs", "outputs", "pipeline_repo", "release_tag", "input_parameters_config", "input_params")
    class PipelineRepo(_message.Message):
        __slots__ = ("name", "url", "secret_location")
        NAME_FIELD_NUMBER: _ClassVar[int]
        URL_FIELD_NUMBER: _ClassVar[int]
        SECRET_LOCATION_FIELD_NUMBER: _ClassVar[int]
        name: str
        url: str
        secret_location: str
        def __init__(self, name: _Optional[str] = ..., url: _Optional[str] = ..., secret_location: _Optional[str] = ...) -> None: ...
    class InputParams(_message.Message):
        __slots__ = ("type", "entity_config", "allow_multiple", "required")
        class EntityConfig(_message.Message):
            __slots__ = ("data_type",)
            DATA_TYPE_FIELD_NUMBER: _ClassVar[int]
            data_type: str
            def __init__(self, data_type: _Optional[str] = ...) -> None: ...
        TYPE_FIELD_NUMBER: _ClassVar[int]
        ENTITY_CONFIG_FIELD_NUMBER: _ClassVar[int]
        ALLOW_MULTIPLE_FIELD_NUMBER: _ClassVar[int]
        REQUIRED_FIELD_NUMBER: _ClassVar[int]
        type: str
        entity_config: Pipeline.InputParams.EntityConfig
        allow_multiple: bool
        required: bool
        def __init__(self, type: _Optional[str] = ..., entity_config: _Optional[_Union[Pipeline.InputParams.EntityConfig, _Mapping]] = ..., allow_multiple: bool = ..., required: bool = ...) -> None: ...
    class InputParametersConfigEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: Pipeline.InputParams
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[Pipeline.InputParams, _Mapping]] = ...) -> None: ...
    class InputParamsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: PipelineInputConfig
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[PipelineInputConfig, _Mapping]] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    VERSION_NUMBER_FIELD_NUMBER: _ClassVar[int]
    BATCH_QUEUE_ARN_FIELD_NUMBER: _ClassVar[int]
    ENTRY_FIELD_NUMBER: _ClassVar[int]
    INPUTS_FIELD_NUMBER: _ClassVar[int]
    OUTPUTS_FIELD_NUMBER: _ClassVar[int]
    PIPELINE_REPO_FIELD_NUMBER: _ClassVar[int]
    RELEASE_TAG_FIELD_NUMBER: _ClassVar[int]
    INPUT_PARAMETERS_CONFIG_FIELD_NUMBER: _ClassVar[int]
    INPUT_PARAMS_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    description: str
    created_at: _timestamp_pb2.Timestamp
    version: str
    version_number: int
    batch_queue_arn: str
    entry: str
    inputs: _containers.RepeatedCompositeFieldContainer[PipelineAttribute]
    outputs: _containers.RepeatedCompositeFieldContainer[PipelineAttribute]
    pipeline_repo: Pipeline.PipelineRepo
    release_tag: str
    input_parameters_config: _containers.MessageMap[str, Pipeline.InputParams]
    input_params: _containers.MessageMap[str, PipelineInputConfig]
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., version: _Optional[str] = ..., version_number: _Optional[int] = ..., batch_queue_arn: _Optional[str] = ..., entry: _Optional[str] = ..., inputs: _Optional[_Iterable[_Union[PipelineAttribute, _Mapping]]] = ..., outputs: _Optional[_Iterable[_Union[PipelineAttribute, _Mapping]]] = ..., pipeline_repo: _Optional[_Union[Pipeline.PipelineRepo, _Mapping]] = ..., release_tag: _Optional[str] = ..., input_parameters_config: _Optional[_Mapping[str, Pipeline.InputParams]] = ..., input_params: _Optional[_Mapping[str, PipelineInputConfig]] = ...) -> None: ...

class CreatePipelineRequest(_message.Message):
    __slots__ = ("name", "description", "version", "version_number", "batch_queue_arn", "entry", "pipeline_repo", "input_parameters_config")
    class PipelineRepo(_message.Message):
        __slots__ = ("new_pipeline_repo", "existing_pipeline_repo", "release_tag", "base_code_location")
        class CreateNewPipelineRepo(_message.Message):
            __slots__ = ("repo_name", "pipeline_repo_url", "access_token")
            REPO_NAME_FIELD_NUMBER: _ClassVar[int]
            PIPELINE_REPO_URL_FIELD_NUMBER: _ClassVar[int]
            ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
            repo_name: str
            pipeline_repo_url: str
            access_token: str
            def __init__(self, repo_name: _Optional[str] = ..., pipeline_repo_url: _Optional[str] = ..., access_token: _Optional[str] = ...) -> None: ...
        class ExistingPipelineRepo(_message.Message):
            __slots__ = ("repo_name",)
            REPO_NAME_FIELD_NUMBER: _ClassVar[int]
            repo_name: str
            def __init__(self, repo_name: _Optional[str] = ...) -> None: ...
        NEW_PIPELINE_REPO_FIELD_NUMBER: _ClassVar[int]
        EXISTING_PIPELINE_REPO_FIELD_NUMBER: _ClassVar[int]
        RELEASE_TAG_FIELD_NUMBER: _ClassVar[int]
        BASE_CODE_LOCATION_FIELD_NUMBER: _ClassVar[int]
        new_pipeline_repo: CreatePipelineRequest.PipelineRepo.CreateNewPipelineRepo
        existing_pipeline_repo: CreatePipelineRequest.PipelineRepo.ExistingPipelineRepo
        release_tag: str
        base_code_location: str
        def __init__(self, new_pipeline_repo: _Optional[_Union[CreatePipelineRequest.PipelineRepo.CreateNewPipelineRepo, _Mapping]] = ..., existing_pipeline_repo: _Optional[_Union[CreatePipelineRequest.PipelineRepo.ExistingPipelineRepo, _Mapping]] = ..., release_tag: _Optional[str] = ..., base_code_location: _Optional[str] = ...) -> None: ...
    class CreatePipelineInputParam(_message.Message):
        __slots__ = ("type", "allow_multiple", "required")
        TYPE_FIELD_NUMBER: _ClassVar[int]
        ALLOW_MULTIPLE_FIELD_NUMBER: _ClassVar[int]
        REQUIRED_FIELD_NUMBER: _ClassVar[int]
        type: str
        allow_multiple: bool
        required: bool
        def __init__(self, type: _Optional[str] = ..., allow_multiple: bool = ..., required: bool = ...) -> None: ...
    class InputParametersConfigEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: CreatePipelineRequest.CreatePipelineInputParam
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[CreatePipelineRequest.CreatePipelineInputParam, _Mapping]] = ...) -> None: ...
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    VERSION_NUMBER_FIELD_NUMBER: _ClassVar[int]
    BATCH_QUEUE_ARN_FIELD_NUMBER: _ClassVar[int]
    ENTRY_FIELD_NUMBER: _ClassVar[int]
    PIPELINE_REPO_FIELD_NUMBER: _ClassVar[int]
    INPUT_PARAMETERS_CONFIG_FIELD_NUMBER: _ClassVar[int]
    name: str
    description: str
    version: str
    version_number: int
    batch_queue_arn: str
    entry: str
    pipeline_repo: CreatePipelineRequest.PipelineRepo
    input_parameters_config: _containers.MessageMap[str, CreatePipelineRequest.CreatePipelineInputParam]
    def __init__(self, name: _Optional[str] = ..., description: _Optional[str] = ..., version: _Optional[str] = ..., version_number: _Optional[int] = ..., batch_queue_arn: _Optional[str] = ..., entry: _Optional[str] = ..., pipeline_repo: _Optional[_Union[CreatePipelineRequest.PipelineRepo, _Mapping]] = ..., input_parameters_config: _Optional[_Mapping[str, CreatePipelineRequest.CreatePipelineInputParam]] = ...) -> None: ...

class PipelineOptionPutRequest(_message.Message):
    __slots__ = ("label", "filename", "benchling_result_table", "action")
    LABEL_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    BENCHLING_RESULT_TABLE_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    label: str
    filename: str
    benchling_result_table: str
    action: PipelineOptionAction
    def __init__(self, label: _Optional[str] = ..., filename: _Optional[str] = ..., benchling_result_table: _Optional[str] = ..., action: _Optional[_Union[PipelineOptionAction, str]] = ...) -> None: ...

class PipelineOptionPutResponse(_message.Message):
    __slots__ = ("object", "label", "action")
    OBJECT_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    object: _data_type_pb2.S3File
    label: str
    action: PipelineOptionAction
    def __init__(self, object: _Optional[_Union[_data_type_pb2.S3File, _Mapping]] = ..., label: _Optional[str] = ..., action: _Optional[_Union[PipelineOptionAction, str]] = ...) -> None: ...

class PipelineRunValue(_message.Message):
    __slots__ = ("string", "int", "double", "boolean", "s3_file", "entity", "entities", "file_upload")
    STRING_FIELD_NUMBER: _ClassVar[int]
    INT_FIELD_NUMBER: _ClassVar[int]
    DOUBLE_FIELD_NUMBER: _ClassVar[int]
    BOOLEAN_FIELD_NUMBER: _ClassVar[int]
    S3_FILE_FIELD_NUMBER: _ClassVar[int]
    ENTITY_FIELD_NUMBER: _ClassVar[int]
    ENTITIES_FIELD_NUMBER: _ClassVar[int]
    FILE_UPLOAD_FIELD_NUMBER: _ClassVar[int]
    string: str
    int: int
    double: float
    boolean: bool
    s3_file: _data_type_pb2.S3File
    entity: _entity_pb2.Entity
    entities: _entity_pb2.EntityList
    file_upload: _data_type_pb2.FileUpload
    def __init__(self, string: _Optional[str] = ..., int: _Optional[int] = ..., double: _Optional[float] = ..., boolean: bool = ..., s3_file: _Optional[_Union[_data_type_pb2.S3File, _Mapping]] = ..., entity: _Optional[_Union[_entity_pb2.Entity, _Mapping]] = ..., entities: _Optional[_Union[_entity_pb2.EntityList, _Mapping]] = ..., file_upload: _Optional[_Union[_data_type_pb2.FileUpload, _Mapping]] = ...) -> None: ...

class PipelineAttribute(_message.Message):
    __slots__ = ("name", "type", "data_type_unique_id", "options")
    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        INVALID: _ClassVar[PipelineAttribute.Type]
        STRING: _ClassVar[PipelineAttribute.Type]
        INT: _ClassVar[PipelineAttribute.Type]
        FLOAT: _ClassVar[PipelineAttribute.Type]
        TIMESTAMP: _ClassVar[PipelineAttribute.Type]
        ENTITY: _ClassVar[PipelineAttribute.Type]
        S3_FILE: _ClassVar[PipelineAttribute.Type]
        FASTQ: _ClassVar[PipelineAttribute.Type]
        BCL: _ClassVar[PipelineAttribute.Type]
        ENTITY_LIST: _ClassVar[PipelineAttribute.Type]
    INVALID: PipelineAttribute.Type
    STRING: PipelineAttribute.Type
    INT: PipelineAttribute.Type
    FLOAT: PipelineAttribute.Type
    TIMESTAMP: PipelineAttribute.Type
    ENTITY: PipelineAttribute.Type
    S3_FILE: PipelineAttribute.Type
    FASTQ: PipelineAttribute.Type
    BCL: PipelineAttribute.Type
    ENTITY_LIST: PipelineAttribute.Type
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    DATA_TYPE_UNIQUE_ID_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    name: str
    type: PipelineAttribute.Type
    data_type_unique_id: str
    options: _containers.RepeatedCompositeFieldContainer[PipelineAttributeOption]
    def __init__(self, name: _Optional[str] = ..., type: _Optional[_Union[PipelineAttribute.Type, str]] = ..., data_type_unique_id: _Optional[str] = ..., options: _Optional[_Iterable[_Union[PipelineAttributeOption, _Mapping]]] = ...) -> None: ...

class PipelineAttributeOption(_message.Message):
    __slots__ = ("label", "value", "benchling_result_table", "archived")
    LABEL_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    BENCHLING_RESULT_TABLE_FIELD_NUMBER: _ClassVar[int]
    ARCHIVED_FIELD_NUMBER: _ClassVar[int]
    label: str
    value: PipelineRunValue
    benchling_result_table: str
    archived: bool
    def __init__(self, label: _Optional[str] = ..., value: _Optional[_Union[PipelineRunValue, _Mapping]] = ..., benchling_result_table: _Optional[str] = ..., archived: bool = ...) -> None: ...

class PipelineWorkflowStep(_message.Message):
    __slots__ = ("name", "description", "order", "inputs", "outputs")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    ORDER_FIELD_NUMBER: _ClassVar[int]
    INPUTS_FIELD_NUMBER: _ClassVar[int]
    OUTPUTS_FIELD_NUMBER: _ClassVar[int]
    name: str
    description: str
    order: int
    inputs: _containers.RepeatedCompositeFieldContainer[PipelineAttribute]
    outputs: _containers.RepeatedCompositeFieldContainer[PipelineAttribute]
    def __init__(self, name: _Optional[str] = ..., description: _Optional[str] = ..., order: _Optional[int] = ..., inputs: _Optional[_Iterable[_Union[PipelineAttribute, _Mapping]]] = ..., outputs: _Optional[_Iterable[_Union[PipelineAttribute, _Mapping]]] = ...) -> None: ...
