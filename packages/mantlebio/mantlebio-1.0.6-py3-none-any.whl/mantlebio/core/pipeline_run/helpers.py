from pathlib import Path
from typing import Any, Dict, List, Optional
from mantlebio.exceptions import MantleTypeError

from proto import data_type_pb2, entity_pb2, pipeline_pb2
from google.protobuf.internal import type_checkers

class MantlePipelineRunKickoff:
    """
    Represents the kickoff of a Mantle pipeline run.

    Args:
        pipeline_id (str): The ID of the pipeline.
        pipeline_version (str): The version of the pipeline.
        external (bool): Indicates whether the pipeline is external or not.
        inputs (Optional[Dict], optional): The inputs for the pipeline run. Defaults to None.
    """

    def __init__(self, pipeline_id: str, pipeline_version: str, external: bool, inputs: Optional[Dict] = None) -> None:
        self.pipeline_id = pipeline_id
        self.pipeline_version = pipeline_version
        self.external = external
        self.inputs = inputs or {}

def validate_pipeline_run_value(value: Any) -> Dict[str, Any]:
    '''Validate a value against a oneof proto field and automatically associate it with the correct keyword.

    Args:
        value (any): any value which is intended to be passed as the value in a key:value pair to a Proto oneOf field

        one_of_proto_field_descriptor (descriptor.OneofDescriptor): The proto description of a one of field. contains
         information about the optional inputs.

    Returns:
        Dict[str, any]: A dictionary containing a single key:value pair which can be passed to the Proto instantiation
         as a valid oneOf option

    Raises:
        TypeError when the supplied value is not of an allowed type for the given one_of_proto_field_descriptor.
    '''
    one_of_proto_field_descriptor = pipeline_pb2.PipelineRunValue.DESCRIPTOR.oneofs[0]
    all_field_names = [f.name for f in one_of_proto_field_descriptor.fields]
    # checkers for types not defined in protobuf internals
    # many fields will return the same type int(11) from proto which indicates a
    # message type. for each of these we will need a new case in this method
    
    if type(value) == entity_pb2.Entity and "entity" in all_field_names:
        return {"entity": value}

    if type(value) == entity_pb2.EntityList and "entities" in all_field_names:
        return {"entities": value}

    if type(value) == data_type_pb2.S3File and "s3_file" in all_field_names:
        return {"s3_file": value}

    if type(value) == data_type_pb2.FileUpload and "file_upload" in all_field_names:
        local_path = Path(value.filename)
        if not local_path.exists():
            raise FileNotFoundError(f"File {local_path} does not exist")
        if local_path.is_dir() and value.filename[-1] != "/":
            value.filename += "/"
        
        return {"file_upload": value}

    if type(value) == bool and "boolean" in all_field_names:
        # type checker doesnt distinguish between bool and int, so we have to here
        return {"boolean": value}
    
    if type(value) == str and "string" in all_field_names:
        # typechecker does not pick up str type, so we have to here
        return {"string": value}
    
    if isinstance(value,int) and "int" in all_field_names:
        return {"int": value}
    
    if type(value) == float and "double" in all_field_names:
        return {"double": value}
    
    
    for field in one_of_proto_field_descriptor.fields:
        n = field.name
        try:
            checker = type_checkers.TypeChecker(field)
            new_val = checker.CheckValue(value)
            return {n: new_val}
        except (TypeError, KeyError) as e:
            if isinstance(e, TypeError):
                # so we tried to check the wrong type. thats ok, we're doing this
                # iteratively and will raise an error for all attempts besides the correct one
                continue
            else:
                # we tried to check for some other proto object type that isnt
                # specified in this list of oneof options
                continue

    raise MantleTypeError(type(value))