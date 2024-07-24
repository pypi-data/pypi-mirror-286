from pathlib import Path
from typing import Any, Dict, List, Mapping, Tuple
from google.protobuf.message import Message
from google.protobuf.json_format import ParseDict
from google.protobuf.message import DecodeError
from mantlebio.exceptions import MantleProtoError, MantleInvalidParameterError, MantleTypeError
from mantlebio.helpers.decorators import deprecated
from proto import data_type_pb2, entity_pb2
from google.protobuf.internal import type_checkers


MAX_REURSION_DEPTH = 10


@deprecated("2.0.0", "use unmarshall_dataset instead")
def unmarshall_entity_proto(proto_content: bytes) -> entity_pb2.Entity:
    return unmarshall_dataset(proto_content)


def unmarshall_dataset(proto_content: bytes) -> entity_pb2.Entity:
    try:
        dataset_response = entity_pb2.EntityResponse()
        dataset_response.ParseFromString(proto_content)
        return dataset_response.entity
    except DecodeError as e:
        raise MantleProtoError(
            proto_content, entity_pb2.EntityResponse)


def data_value_to_dict(key: str, data_value: entity_pb2.EntityDataValue) -> Dict[str, Any]:
    if data_value.HasField("string"):
        return {key: data_value.string}
    if data_value.HasField("int"):
        return {key: data_value.int}
    if data_value.HasField("double"):
        return {key: data_value.double}
    if data_value.HasField("boolean"):
        return {key: data_value.boolean}
    if data_value.HasField("s3_file"):
        return {f"{key}": f"s3://{data_value.s3_file.bucket}/{data_value.s3_file.key}"}
    if data_value.HasField("entity"):
        return {f"{key}_unique_id": data_value.entity.unique_id}
    if data_value.HasField("file_upload"):
        return {key: data_value.file_upload}
    if data_value.HasField("object"):
        return {key: "Unsupported Type"}

    raise MantleTypeError("Data value type not supported")


@deprecated("2.0.0", "use validate_dataset_data_value instead")
def validate_entity_data_value(value: Any, create: bool = False, depth: int = 0) -> Dict[str, Any]:
    return validate_dataset_data_value(value, create, depth)


def validate_dataset_data_value(value: Any, create: bool = False, depth: int = 0) -> Dict[str, Any]:
    '''Validate a value against a oneof proto field and automatically associate it with the correct keyword.

    Args:
        value (Any): Any value which is intended to be passed as the value in a key:value pair to a Proto oneOf field.
                     This can be a direct instance of the Protobuf message or a JSON string representation of it

    Returns:
        Dict[str, Any]: A dictionary containing a single key:value pair which can be passed to the Proto instantiation
                        as a valid oneOf option

    Raises:
        TypeError when the supplied value is not of an allowed type for the given one_of_proto_field_descriptor.
    '''
    data_value_type = entity_pb2.CreateEntityDataValue if create else entity_pb2.EntityDataValue
    one_of_proto_field_descriptor = data_value_type.DESCRIPTOR.oneofs[0]
    all_field_names = [f.name for f in one_of_proto_field_descriptor.fields]

    # Check for direct instances of the Protobuf messages
    if type(value) == entity_pb2.Entity and "entity" in all_field_names:
        return {"entity": value}

    if type(value) == data_type_pb2.S3File and "s3_file" in all_field_names:
        return {"s3_file": value}

    if type(value) == bool and "boolean" in all_field_names:
        return {"boolean": value}

    if type(value) == data_type_pb2.FileUpload and "file_upload" in all_field_names:
        local_path = Path(value.filename)
        if not local_path.exists():
            raise FileNotFoundError(f"File {local_path} does not exist")
        if local_path.is_dir() and value.filename[-1] != "/":
            value.filename += "/"
        return {"file_upload": value}
    if type(value) == str:
        # Check if its an S3 URI
        if value.startswith("s3://") and "s3_file" in all_field_names:
            bucket = value.split("/")[2]
            key = "/".join(value.split("/")[3:])
            return {"s3_file": data_type_pb2.S3File(bucket=bucket, key=key)}
        if "string" in all_field_names:
            return {"string": value}
    if isinstance(value, int) and "int" in all_field_names:
        return {"int": value}
    if type(value) == float and "double" in all_field_names:
        return {"double": value}

    if isinstance(value, List):
        return {"list": data_value_type.List(values=[validate_dataset_data_value(item, create, depth+1) for item in value])}

    if isinstance(value, Mapping):
        if create:
            return {"object": entity_pb2.CreateEntityDataValue.DataObject(values={k: entity_pb2.CreateEntityDataValue(**validate_dataset_data_value(v, create, depth+1)) for k, v in value.items()})}
        return {"object": entity_pb2.EntityDataValue.DataObject(values={k: entity_pb2.EntityDataValue(**validate_dataset_data_value(v, create, depth+1)) for k, v in value.items()})}

    for field in one_of_proto_field_descriptor.fields:
        try:
            checker = type_checkers.TypeChecker(field)
            new_val = checker.CheckValue(value)
            return {field.name: new_val}
        except (TypeError, KeyError):
            continue

    raise MantleTypeError(type(value))


@deprecated("2.0.0", "use dataset_params_from_json instead")
def entity_pb2_params_from_json(json: Dict[str, Any]) -> dict:
    return dataset_params_from_json(json)


def dataset_params_from_json(json: Dict[str, Any]) -> dict:
    if json.get("props"):
        prop_dict = json.pop("props")
        dataset_property_obj = DatasetPropertiesBuilder().build_dataset_props(prop_dict)
        json["props"] = dataset_property_obj
        return json
    elif json.get("properties"):
        prop_dict = json.pop("properties")
        dataset_property_obj = DatasetPropertiesBuilder().build_dataset_props(prop_dict)
        json["properties"] = dataset_property_obj
    return json


class DatasetDataValueBuilder:
    def __init__(self):
        pass

    def build_dataset_data_value(self, val: Any) -> entity_pb2.EntityDataValue:
        if isinstance(val, Message):
            one_of_kwarg = validate_dataset_data_value(value=val)
            return entity_pb2.EntityDataValue(**one_of_kwarg)
        elif isinstance(val, dict):
            return ParseDict(val, entity_pb2.EntityDataValue())
        else:
            raise MantleInvalidParameterError(
                f"Invalid type for dataset property value: {type(val)}")


class EntityDataValueBuilder(DatasetDataValueBuilder):
    @deprecated("2.0.0", "Use DatasetDataValueBuilder instead")
    def __init__(self):
        super().__init__()

    def build_entity_data_value(self, val: Any) -> entity_pb2.EntityDataValue:
        return super().build_dataset_data_value(val)


class CreateDatasetDataValueBuilder:
    def __init__(self):
        pass

    def build_create_dataset_data_value(self, val: Any) -> entity_pb2.CreateEntityDataValue:
        if isinstance(val, dict):
            return ParseDict(val, entity_pb2.CreateEntityDataValue())
        else:
            one_of_kwarg = validate_dataset_data_value(value=val, create=True)
            return entity_pb2.CreateEntityDataValue(**one_of_kwarg)


class CreateEntityDataValueBuilder(CreateDatasetDataValueBuilder):
    @deprecated("2.0.0", "Use CreateDatasetDataValueBuilder instead")
    def __init__(self):
        super().__init__()

    @deprecated("2.0.0", "Use build_create_dataset_data_value instead")
    def build_create_entity_data_value(self, val: Any) -> entity_pb2.CreateEntityDataValue:
        return super().build_create_dataset_data_value(val)


class DatasetPropertiesBuilder:
    def __init__(self):
        self.dataset_data_value_builder = DatasetDataValueBuilder()
        self.create_dataset_data_value_builder = CreateDatasetDataValueBuilder()

    def build_dataset_props(self, props: dict) -> Mapping[str, entity_pb2.EntityDataValue]:
        return {key: self.dataset_data_value_builder.build_dataset_data_value(val) for key, val in props.items()}

    def build_create_dataset_props(self, props: dict) -> Mapping[str, entity_pb2.CreateEntityDataValue]:
        return {key: self.create_dataset_data_value_builder.build_create_dataset_data_value(val) for key, val in props.items()}

    def convert_create_dataset_props(self, props: Mapping[str, entity_pb2.EntityDataValue]) -> Mapping[str, entity_pb2.CreateEntityDataValue]:
        return {key: self.convert_create_dataset_data_value(val) for key, val in props.items()}

    def convert_create_dataset_data_value(self, val: entity_pb2.EntityDataValue, depth=0) -> entity_pb2.CreateEntityDataValue:
        if depth > MAX_REURSION_DEPTH:
            raise MantleInvalidParameterError("Recursion depth exceeded")
        if val.HasField("string"):
            return entity_pb2.CreateEntityDataValue(string=val.string)
        if val.HasField("int"):
            return entity_pb2.CreateEntityDataValue(int=val.int)
        if val.HasField("double"):
            return entity_pb2.CreateEntityDataValue(double=val.double)
        if val.HasField("boolean"):
            return entity_pb2.CreateEntityDataValue(boolean=val.boolean)
        if val.HasField("s3_file"):
            return entity_pb2.CreateEntityDataValue(s3_file=val.s3_file)
        if val.HasField("entity"):
            return entity_pb2.CreateEntityDataValue(entity=val.entity)
        if val.HasField("list"):
            return entity_pb2.CreateEntityDataValue(list=entity_pb2.CreateEntityDataValue.List(values=[self.convert_create_dataset_data_value(v, depth+1) for v in val.list.values]))
        if val.HasField("file_upload"):
            local_path = Path(val.file_upload.filename)
            if not local_path.exists():
                raise FileNotFoundError(f"File {local_path} does not exist")
            if local_path.is_dir() and val.file_upload.filename[-1] != "/":
                val.file_upload.filename += "/"
            return entity_pb2.CreateEntityDataValue(file_upload=val.file_upload)
        if val.HasField("object"):
            return entity_pb2.CreateEntityDataValue(object=entity_pb2.CreateEntityDataValue.DataObject(values={k: self.convert_create_dataset_data_value(v, depth+1) for k, v in val.object.values.items()}))

        return entity_pb2.CreateEntityDataValue()


class EntityPropertiesBuilder(DatasetPropertiesBuilder):
    @deprecated("2.0.0", "Use DatasetPropertiesBuilder instead")
    def __init__(self):
        super().__init__()

    def build_entity_props(self, props: dict) -> Mapping[str, entity_pb2.EntityDataValue]:
        return super().build_dataset_props(props)

    def build_create_entity_props(self, props: dict) -> Mapping[str, entity_pb2.CreateEntityDataValue]:
        return super().build_create_dataset_props(props)

    def convert_create_entity_props(self, props: Mapping[str, entity_pb2.EntityDataValue]) -> Mapping[str, entity_pb2.CreateEntityDataValue]:
        return super().convert_create_dataset_props(props)

    def convert_create_entity_data_value(self, val: entity_pb2.EntityDataValue, depth=0) -> entity_pb2.CreateEntityDataValue:
        return super().convert_create_dataset_data_value(val, depth)
