import os
from typing import Mapping
import unittest
from mantlebio.core.dataset.helpers import (
    EntityDataValueBuilder,
    EntityPropertiesBuilder,
    data_value_to_dict,
    entity_pb2_params_from_json,
    unmarshall_dataset,
    unmarshall_entity_proto,
    validate_dataset_data_value,
    dataset_params_from_json,
    DatasetDataValueBuilder,
    DatasetPropertiesBuilder,
    validate_entity_data_value,
)
from mantlebio.exceptions import (
    MantleProtoError,
    MantleInvalidParameterError,
    MantleTypeError,
)
from proto import data_type_pb2, entity_pb2


class TestDatasetHelpers(unittest.TestCase):

    def setUp(self):
        os.mkdir(f"{os.getcwd()}/test_folder")
        with open(f"{os.getcwd()}/test_folder/test_upload.txt", "w") as f:
            f.write("test content")
    
    def tearDown(self):
        os.remove(f"{os.getcwd()}/test_folder/test_upload.txt")
        os.rmdir(f"{os.getcwd()}/test_folder")


    def test_unmarshall_dataset(self):
        proto_content = entity_pb2.EntityResponse().SerializeToString()
        dataset = unmarshall_dataset(proto_content)
        self.assertIsInstance(dataset, entity_pb2.Entity)

    def test_validate_dataset_data_value_with_entity(self):
        value = entity_pb2.Entity()
        result = validate_dataset_data_value(value)
        self.assertEqual(result, {"entity": value})

    def test_validate_dataset_data_value_with_s3_file(self):
        value = data_type_pb2.S3File()
        result = validate_dataset_data_value(value)
        self.assertEqual(result, {"s3_file": value})

    def test_validate_dataset_data_value_with_bool(self):
        value = True
        result = validate_dataset_data_value(value)
        self.assertEqual(result, {"boolean": value})

    def test_validate_dataset_data_value_with_file_upload(self):
        value = data_type_pb2.FileUpload(
            filename="test_folder",
        )
        expected_value = data_type_pb2.FileUpload(
            filename="test_folder/",
        )
        result = validate_dataset_data_value(value)
        self.assertEqual(result, {"file_upload": expected_value})

    def test_validate_dataset_data_value_with_string(self):
        value = "test_string"
        result = validate_dataset_data_value(value)
        self.assertEqual(result, {"string": value})
    
    def test_validate_dataset_data_value_with_object_type(self):
        value = {"key": "value"}
        result = validate_dataset_data_value(value)
        self.assertEqual(result,{"object": entity_pb2.EntityDataValue.DataObject(values={"key":entity_pb2.EntityDataValue(string="value")})})

    def test_build_dataset_data_value_with_message(self):
        builder = DatasetDataValueBuilder()
        value = entity_pb2.Entity()
        result = builder.build_dataset_data_value(value)
        self.assertIsInstance(result, entity_pb2.EntityDataValue)
        self.assertEqual(result.entity, value)

    def test_build_datset_data_value_with_dict(self):
        builder = DatasetDataValueBuilder()
        value = {"string":"value"}
        result = builder.build_dataset_data_value(value)
        self.assertIsInstance(result, entity_pb2.EntityDataValue)
        self.assertEqual(result.string, "value")
    
    def test_build_dataset_data_value_with_invalid_type(self):
        builder = DatasetDataValueBuilder()
        value = []
        with self.assertRaises(MantleInvalidParameterError):
            builder.build_dataset_data_value(value)

    def test_dataset_params_from_json_with_properties(self):
        json = {
            "properties": {
                "key1": {"string":"value1"},
                "key2": {"string":"value2"}
            }
        }
        expected_result = {
            "properties": {"key1": entity_pb2.EntityDataValue(string="value1"),"key2": entity_pb2.EntityDataValue(string="value2")}
        }
        result = dataset_params_from_json(json)
        self.assertEqual(result, expected_result)

    def test_dataset_params_from_json_without_properties(self):
        json = {
            "other_key": "other_value"
        }
        expected_result = {
            "other_key": "other_value"
        }
        result = dataset_params_from_json(json)
        self.assertEqual(result, expected_result)

    def test_build_dataset_props(self):
        builder = DatasetPropertiesBuilder()
        props = {
            "key1": {"string":"value1"},
            "key2": entity_pb2.Entity()
        }
        result = builder.build_dataset_props(props)
        self.assertEqual(result["key1"].string, "value1")
        self.assertEqual(result["key2"].entity, entity_pb2.Entity())

    def test_convert_create_dataset_data_value_string(self):
        builder = DatasetPropertiesBuilder()
        val = entity_pb2.EntityDataValue(string="value")
        result = builder.convert_create_dataset_data_value(val)
        self.assertIsInstance(result, entity_pb2.CreateEntityDataValue)
        self.assertEqual(result.string, "value")

    def test_convert_create_dataset_data_value_int(self):
        builder = DatasetPropertiesBuilder()
        val = entity_pb2.EntityDataValue(int=1)
        result = builder.convert_create_dataset_data_value(val)
        self.assertIsInstance(result, entity_pb2.CreateEntityDataValue)
        self.assertEqual(result.int, 1)

    def test_convert_create_dataset_data_value_double(self):
        builder = DatasetPropertiesBuilder()
        val = entity_pb2.EntityDataValue(double=1.0)
        result = builder.convert_create_dataset_data_value(val)
        self.assertIsInstance(result, entity_pb2.CreateEntityDataValue)
        self.assertEqual(result.double, 1.0)

    def test_convert_create_dataset_data_value_boolean(self):
        builder = DatasetPropertiesBuilder()
        val = entity_pb2.EntityDataValue(boolean=True)
        result = builder.convert_create_dataset_data_value(val)
        self.assertIsInstance(result, entity_pb2.CreateEntityDataValue)
        self.assertEqual(result.boolean, True)

    def test_convert_create_dataset_data_value_s3_file(self):
        builder = DatasetPropertiesBuilder()
        val = entity_pb2.EntityDataValue(s3_file=data_type_pb2.S3File())
        result = builder.convert_create_dataset_data_value(val)
        self.assertIsInstance(result, entity_pb2.CreateEntityDataValue)
        self.assertIsInstance(result.s3_file, data_type_pb2.S3File)
        self.assertEqual(result.s3_file, data_type_pb2.S3File())

    def test_convert_create_dataset_data_value_entity(self):
        builder = DatasetPropertiesBuilder()
        val = entity_pb2.EntityDataValue(entity=entity_pb2.Entity())
        result = builder.convert_create_dataset_data_value(val)
        self.assertIsInstance(result, entity_pb2.CreateEntityDataValue)
        self.assertIsInstance(result.entity, entity_pb2.Entity)
        self.assertEqual(result.entity, entity_pb2.Entity())

    def test_convert_create_dataset_data_value_list(self):
        builder = DatasetPropertiesBuilder()
        val = entity_pb2.EntityDataValue(list=entity_pb2.EntityDataValue.List(values=[entity_pb2.EntityDataValue(string="value"),entity_pb2.EntityDataValue(int=1)]))
        result = builder.convert_create_dataset_data_value(val)
        self.assertIsInstance(result, entity_pb2.CreateEntityDataValue)
        self.assertIsInstance(result.list, entity_pb2.CreateEntityDataValue.List)
        self.assertEqual(result.list.values[0].string, "value")
        self.assertEqual(result.list.values[1].int, 1)

    def test_convert_create_dataset_data_value_list_max_depth(self):
        builder = DatasetPropertiesBuilder()
        val = entity_pb2.EntityDataValue(
            list=entity_pb2.EntityDataValue.List(
                values=[entity_pb2.EntityDataValue(
                    list=entity_pb2.EntityDataValue.List(
                        values=[entity_pb2.EntityDataValue(
                            list=entity_pb2.EntityDataValue.List(
                                values=[entity_pb2.EntityDataValue(
                                    list=entity_pb2.EntityDataValue.List(
                                        values=[entity_pb2.EntityDataValue(
                                            list=entity_pb2.EntityDataValue.List(
                                                values=[entity_pb2.EntityDataValue(
                                                    list=entity_pb2.EntityDataValue.List(
                                                        values=[entity_pb2.EntityDataValue(
                                                            list=entity_pb2.EntityDataValue.List(
                                                                values=[entity_pb2.EntityDataValue(
                                                                    list=entity_pb2.EntityDataValue.List(
                                                                        values=[entity_pb2.EntityDataValue(
                                                                            list=entity_pb2.EntityDataValue.List(
                                                                                values=[entity_pb2.EntityDataValue(
                                                                                    list=entity_pb2.EntityDataValue.List(
                                                                                        values=[entity_pb2.EntityDataValue(
                                                                                            list=entity_pb2.EntityDataValue.List (
                                                                                                values = [entity_pb2.EntityDataValue(string="testing")]
                                                                                            )
                                                                                        )]
                                                                                           
                                                                                    )
                                                                                )] 
                                                                            )
                                                                        )]
                                                                    )
                                                                )]
                                                            )
                                                                    
                                                        )]
                                                    )
                                                )]
                                            )
                                        )]
                                    )
                                )]
                            )
                        )]
                    )
                )]
            )
        )
        with self.assertRaises(MantleInvalidParameterError):
            builder.convert_create_dataset_data_value(val)

    def test_convert_create_dataset_data_value_file_upload(self):
        builder = DatasetPropertiesBuilder()
        val = entity_pb2.EntityDataValue(file_upload=data_type_pb2.FileUpload(
            filename="test_folder",
        ))
        expected_value = data_type_pb2.FileUpload(
            filename="test_folder/",
        )
        result = builder.convert_create_dataset_data_value(val)
        self.assertIsInstance(result, entity_pb2.CreateEntityDataValue)
        self.assertIsInstance(result.file_upload, data_type_pb2.FileUpload)
        self.assertEqual(result.file_upload, expected_value)

    def test_convert_create_dataset_data_value_object(self):
        builder = DatasetPropertiesBuilder()
        val = entity_pb2.EntityDataValue(object=entity_pb2.EntityDataValue.DataObject(values={"key":entity_pb2.EntityDataValue(object=entity_pb2.EntityDataValue.DataObject(values={"key2":entity_pb2.EntityDataValue(string="value")}))}))
        result = builder.convert_create_dataset_data_value(val)
        self.assertIsInstance(result, entity_pb2.CreateEntityDataValue)
        self.assertIsInstance(result.object, entity_pb2.CreateEntityDataValue.DataObject)
        self.assertEqual(result.object, entity_pb2.CreateEntityDataValue.DataObject(values={"key":entity_pb2.CreateEntityDataValue(object=entity_pb2.CreateEntityDataValue.DataObject(values={"key2":entity_pb2.CreateEntityDataValue(string="value")}))}))

    def test_convert_create_dataset_data_value_empty(self):
        builder = DatasetPropertiesBuilder()
        val = entity_pb2.EntityDataValue()
        result = builder.convert_create_dataset_data_value(val)
        self.assertIsInstance(result, entity_pb2.CreateEntityDataValue)
        self.assertEqual(result,entity_pb2.CreateEntityDataValue())
        

    # Tests for Deprecated Functions 
    def test_unmarshall_entity_proto(self):
        proto_content = entity_pb2.EntityResponse().SerializeToString()

        with self.assertWarns(DeprecationWarning) as cm:
            entity = unmarshall_entity_proto(proto_content)
        self.assertEqual(str(cm.warnings[0].message), 'Function unmarshall_entity_proto is deprecated and will be removed in version 2.0.0. use unmarshall_dataset instead')
        self.assertIsInstance(entity, entity_pb2.Entity)

    def test_validate_entity_data_value_with_entity(self):
        value = entity_pb2.Entity()
        with self.assertWarns(DeprecationWarning) as cm:
            result = validate_entity_data_value(value)
        self.assertEqual(str(cm.warnings[0].message), 'Function validate_entity_data_value is deprecated and will be removed in version 2.0.0. use validate_dataset_data_value instead')
        self.assertEqual(result, {"entity": value})

    def test_validate_entity_data_value_with_s3_file(self):
        value = data_type_pb2.S3File()
        with self.assertWarns(DeprecationWarning) as cm:
            result = validate_entity_data_value(value)
        self.assertEqual(str(cm.warnings[0].message), 'Function validate_entity_data_value is deprecated and will be removed in version 2.0.0. use validate_dataset_data_value instead')
        self.assertEqual(result, {"s3_file": value})

    def test_validate_entity_data_value_with_bool(self):
        value = True
        with self.assertWarns(DeprecationWarning) as cm:
            result = validate_entity_data_value(value)
        self.assertEqual(str(cm.warnings[0].message), 'Function validate_entity_data_value is deprecated and will be removed in version 2.0.0. use validate_dataset_data_value instead')
        self.assertEqual(result, {"boolean": value})

    def test_validate_entity_data_value_with_file_upload(self):
        value = data_type_pb2.FileUpload(
            filename="test_folder",
        )
        expected_value = data_type_pb2.FileUpload(
            filename="test_folder/",
        )
        with self.assertWarns(DeprecationWarning) as cm:
            result = validate_entity_data_value(value)
        self.assertEqual(str(cm.warnings[0].message), 'Function validate_entity_data_value is deprecated and will be removed in version 2.0.0. use validate_dataset_data_value instead')
        self.assertEqual(result, {"file_upload": expected_value})

    def test_validate_entity_data_value_with_string(self):
        value = "test_string"
        with self.assertWarns(DeprecationWarning) as cm:
            result = validate_entity_data_value(value)
        self.assertEqual(str(cm.warnings[0].message), 'Function validate_entity_data_value is deprecated and will be removed in version 2.0.0. use validate_dataset_data_value instead')
        self.assertEqual(result, {"string": value})

    def test_validate_entity_data_value_with_object_type(self):
        value = {"key": "value"}
        with self.assertWarns(DeprecationWarning) as cm:
            result = validate_entity_data_value(value)
        self.assertEqual(str(cm.warnings[0].message), 'Function validate_entity_data_value is deprecated and will be removed in version 2.0.0. use validate_dataset_data_value instead')
        self.assertEqual(result,{"object": entity_pb2.EntityDataValue.DataObject(values={"key":entity_pb2.EntityDataValue(string="value")})})
    
    def test_build_entity_data_value_with_message(self):
        with self.assertWarns(DeprecationWarning) as cm:
            builder = EntityDataValueBuilder()
            value = entity_pb2.Entity()
            result = builder.build_dataset_data_value(value)
        self.assertEqual(str(cm.warnings[0].message), 'Class EntityDataValueBuilder is deprecated and will be removed in version 2.0.0. Use DatasetDataValueBuilder instead')
        self.assertIsInstance(result, entity_pb2.EntityDataValue)
        self.assertEqual(result.entity, value)

    def test_build_entity_data_value_with_dict(self):
        with self.assertWarns(DeprecationWarning) as cm:
            builder = EntityDataValueBuilder()
            value = {"string":"value"}
            result = builder.build_dataset_data_value(value)
        self.assertEqual(str(cm.warnings[0].message), 'Class EntityDataValueBuilder is deprecated and will be removed in version 2.0.0. Use DatasetDataValueBuilder instead')
        self.assertIsInstance(result, entity_pb2.EntityDataValue)
        self.assertEqual(result.string, "value")

    def test_build_entity_data_value_with_invalid_type(self):
        with self.assertWarns(DeprecationWarning) as cm:
            builder = EntityDataValueBuilder()
            value = []
            with self.assertRaises(MantleInvalidParameterError):
                builder.build_dataset_data_value(value)
        self.assertEqual(str(cm.warnings[0].message), 'Class EntityDataValueBuilder is deprecated and will be removed in version 2.0.0. Use DatasetDataValueBuilder instead')

    def test_entity_pb2_params_from_json_with_properties(self):
        json = {
            "properties": {
                "key1": {"string":"value1"},
                "key2": {"string":"value2"}
            }
        }
        expected_result = {
            "properties": {"key1": entity_pb2.EntityDataValue(string="value1"),"key2": entity_pb2.EntityDataValue(string="value2")}
        }
        with self.assertWarns(DeprecationWarning) as cm:
            result = entity_pb2_params_from_json(json)
        self.assertEqual(str(cm.warnings[0].message), 'Function entity_pb2_params_from_json is deprecated and will be removed in version 2.0.0. use dataset_params_from_json instead')
        self.assertEqual(result, expected_result)

    def test_entity_pb2_params_from_json_without_properties(self):
        json = {
            "other_key": "other_value"
        }
        expected_result = {
            "other_key": "other_value"
        }
        with self.assertWarns(DeprecationWarning) as cm:
            result = entity_pb2_params_from_json(json)
        self.assertEqual(str(cm.warnings[0].message), 'Function entity_pb2_params_from_json is deprecated and will be removed in version 2.0.0. use dataset_params_from_json instead')
        self.assertEqual(result, expected_result)

    def test_build_entity_props(self):
        with self.assertWarns(DeprecationWarning) as cm:
            builder = EntityPropertiesBuilder()
            props = {
                "key1": {"string":"value1"},
                "key2": entity_pb2.Entity()
            }
            result = builder.build_entity_props(props)
        self.assertEqual(str(cm.warnings[0].message), 'Class EntityPropertiesBuilder is deprecated and will be removed in version 2.0.0. Use DatasetPropertiesBuilder instead')
        self.assertEqual(result["key1"].string, "value1")
        self.assertEqual(result["key2"].entity, entity_pb2.Entity())

    def test_convert_create_entity_data_value_string(self):
        with self.assertWarns(DeprecationWarning) as cm:
            builder = EntityPropertiesBuilder()
            val = entity_pb2.EntityDataValue(string="value")
            result = builder.convert_create_entity_data_value(val)
        self.assertEqual(str(cm.warnings[0].message), 'Class EntityPropertiesBuilder is deprecated and will be removed in version 2.0.0. Use DatasetPropertiesBuilder instead')
        self.assertIsInstance(result, entity_pb2.CreateEntityDataValue)
        self.assertEqual(result.string, "value")

    def test_convert_create_entity_data_value_int(self):
        with self.assertWarns(DeprecationWarning) as cm:
            builder = EntityPropertiesBuilder()
            val = entity_pb2.EntityDataValue(int=1)
            result = builder.convert_create_entity_data_value(val)
        self.assertEqual(str(cm.warnings[0].message), 'Class EntityPropertiesBuilder is deprecated and will be removed in version 2.0.0. Use DatasetPropertiesBuilder instead')
        self.assertIsInstance(result, entity_pb2.CreateEntityDataValue)
        self.assertEqual(result.int, 1)

    def test_convert_create_entity_data_value_double(self):
        with self.assertWarns(DeprecationWarning) as cm:
            builder = EntityPropertiesBuilder()
            val = entity_pb2.EntityDataValue(double=1.0)
            result = builder.convert_create_entity_data_value(val)
        self.assertEqual(str(cm.warnings[0].message), 'Class EntityPropertiesBuilder is deprecated and will be removed in version 2.0.0. Use DatasetPropertiesBuilder instead')
        self.assertIsInstance(result, entity_pb2.CreateEntityDataValue)
        self.assertEqual(result.double, 1.0)

    def test_convert_create_entity_data_value_boolean(self):
        with self.assertWarns(DeprecationWarning) as cm:
            builder = EntityPropertiesBuilder()
            val = entity_pb2.EntityDataValue(boolean=True)
            result = builder.convert_create_entity_data_value(val)
        self.assertEqual(str(cm.warnings[0].message), 'Class EntityPropertiesBuilder is deprecated and will be removed in version 2.0.0. Use DatasetPropertiesBuilder instead')
        self.assertIsInstance(result, entity_pb2.CreateEntityDataValue)
        self.assertEqual(result.boolean, True)

    def test_convert_create_entity_data_value_s3_file(self):
        with self.assertWarns(DeprecationWarning) as cm:
            builder = EntityPropertiesBuilder()
            val = entity_pb2.EntityDataValue(s3_file=data_type_pb2.S3File())
            result = builder.convert_create_entity_data_value(val)
        self.assertEqual(str(cm.warnings[0].message), 'Class EntityPropertiesBuilder is deprecated and will be removed in version 2.0.0. Use DatasetPropertiesBuilder instead')
        self.assertIsInstance(result, entity_pb2.CreateEntityDataValue)
        self.assertIsInstance(result.s3_file, data_type_pb2.S3File)
        self.assertEqual(result.s3_file, data_type_pb2.S3File())

    def test_convert_create_entity_data_value_entity(self):
        with self.assertWarns(DeprecationWarning) as cm:
            builder = EntityPropertiesBuilder()
            val = entity_pb2.EntityDataValue(entity=entity_pb2.Entity())
            result = builder.convert_create_entity_data_value(val)
        self.assertEqual(str(cm.warnings[0].message), 'Class EntityPropertiesBuilder is deprecated and will be removed in version 2.0.0. Use DatasetPropertiesBuilder instead')
        self.assertIsInstance(result, entity_pb2.CreateEntityDataValue)
        self.assertIsInstance(result.entity, entity_pb2.Entity)
        self.assertEqual(result.entity, entity_pb2.Entity())

    def test_convert_create_entity_data_value_list(self):
        with self.assertWarns(DeprecationWarning) as cm:
            builder = EntityPropertiesBuilder()
            val = entity_pb2.EntityDataValue(list=entity_pb2.EntityDataValue.List(values=[entity_pb2.EntityDataValue(string="value"),entity_pb2.EntityDataValue(int=1)]))
            result = builder.convert_create_entity_data_value(val)
        self.assertEqual(str(cm.warnings[0].message), 'Class EntityPropertiesBuilder is deprecated and will be removed in version 2.0.0. Use DatasetPropertiesBuilder instead')
        self.assertIsInstance(result, entity_pb2.CreateEntityDataValue)
        self.assertIsInstance(result.list, entity_pb2.CreateEntityDataValue.List)
        self.assertEqual(result.list.values[0].string, "value")
        self.assertEqual(result.list.values[1].int, 1)

    def test_convert_create_entity_data_value_list_max_depth(self):
        with self.assertWarns(DeprecationWarning) as cm:
            builder = EntityPropertiesBuilder()
            val = entity_pb2.EntityDataValue(
                list=entity_pb2.EntityDataValue.List(
                    values=[entity_pb2.EntityDataValue(
                        list=entity_pb2.EntityDataValue.List(
                            values=[entity_pb2.EntityDataValue(
                                list=entity_pb2.EntityDataValue.List(
                                    values=[entity_pb2.EntityDataValue(
                                        list=entity_pb2.EntityDataValue.List(
                                            values=[entity_pb2.EntityDataValue(
                                                list=entity_pb2.EntityDataValue.List(
                                                    values=[entity_pb2.EntityDataValue(
                                                        list=entity_pb2.EntityDataValue.List(
                                                            values=[entity_pb2.EntityDataValue(
                                                                list=entity_pb2.EntityDataValue.List(
                                                                    values=[entity_pb2.EntityDataValue(
                                                                        list=entity_pb2.EntityDataValue.List(
                                                                            values=[entity_pb2.EntityDataValue(
                                                                                list=entity_pb2.EntityDataValue.List(
                                                                                    values=[entity_pb2.EntityDataValue(
                                                                                        list=entity_pb2.EntityDataValue.List(
                                                                                            values=[entity_pb2.EntityDataValue(
                                                                                                list=entity_pb2.EntityDataValue.List (
                                                                                                    values = [entity_pb2.EntityDataValue(string="testing")]
                                                                                                )
                                                                                            )]
                                                                                            
                                                                                        )
                                                                                    )] 
                                                                                )
                                                                            )]
                                                                        )
                                                                    )]
                                                                )
                                                                        
                                                            )]
                                                        )
                                                    )]
                                                )
                                            )]
                                        )
                                    )]
                                )
                            )]
                        )
                    )]
                )
            )
            with self.assertRaises(MantleInvalidParameterError):
                builder.convert_create_entity_data_value(val)
        self.assertEqual(str(cm.warnings[0].message), 'Class EntityPropertiesBuilder is deprecated and will be removed in version 2.0.0. Use DatasetPropertiesBuilder instead')

    def test_convert_create_entity_data_value_file_upload(self):
        with self.assertWarns(DeprecationWarning) as cm:
            builder = EntityPropertiesBuilder()
            val = entity_pb2.EntityDataValue(file_upload=data_type_pb2.FileUpload(
                filename="test_folder",
            ))
            expected_value = data_type_pb2.FileUpload(
                filename="test_folder/",
            )
            result = builder.convert_create_entity_data_value(val)
        self.assertEqual(str(cm.warnings[0].message), 'Class EntityPropertiesBuilder is deprecated and will be removed in version 2.0.0. Use DatasetPropertiesBuilder instead')
        self.assertIsInstance(result, entity_pb2.CreateEntityDataValue)
        self.assertIsInstance(result.file_upload, data_type_pb2.FileUpload)
        self.assertEqual(result.file_upload, expected_value)

    def test_convert_create_entity_data_value_object(self):
        with self.assertWarns(DeprecationWarning) as cm:
            builder = EntityPropertiesBuilder()
            val = entity_pb2.EntityDataValue(object=entity_pb2.EntityDataValue.DataObject(values={"key":entity_pb2.EntityDataValue(object=entity_pb2.EntityDataValue.DataObject(values={"key2":entity_pb2.EntityDataValue(string="value")}))}))
            result = builder.convert_create_entity_data_value(val)
        self.assertEqual(str(cm.warnings[0].message), 'Class EntityPropertiesBuilder is deprecated and will be removed in version 2.0.0. Use DatasetPropertiesBuilder instead')
        self.assertIsInstance(result, entity_pb2.CreateEntityDataValue)
        self.assertIsInstance(result.object, entity_pb2.CreateEntityDataValue.DataObject)
        self.assertEqual(result.object, entity_pb2.CreateEntityDataValue.DataObject(values={"key":entity_pb2.CreateEntityDataValue(object=entity_pb2.CreateEntityDataValue.DataObject(values={"key2":entity_pb2.CreateEntityDataValue(string="value")}))}))

    def test_convert_create_entity_data_value_empty(self):
        with self.assertWarns(DeprecationWarning) as cm:
            builder = EntityPropertiesBuilder()
            val = entity_pb2.EntityDataValue()
            result = builder.convert_create_entity_data_value(val)
        self.assertEqual(str(cm.warnings[0].message), 'Class EntityPropertiesBuilder is deprecated and will be removed in version 2.0.0. Use DatasetPropertiesBuilder instead')
        self.assertIsInstance(result, entity_pb2.CreateEntityDataValue)
        self.assertEqual(result,entity_pb2.CreateEntityDataValue())
        
    def test_data_value_to_dict_string(self):
       data_value = entity_pb2.EntityDataValue(string="test")
       result = data_value_to_dict("test",data_value)
       assert result == {"test":"test"}

    def test_data_value_to_dict_int(self):
       data_value = entity_pb2.EntityDataValue(int=1)
       result = data_value_to_dict("test",data_value)
       assert result == {"test":1}

    def test_data_value_to_dict_double(self):
        data_value = entity_pb2.EntityDataValue(double=1.0)
        result = data_value_to_dict("test",data_value)
        assert result == {"test":1.0}
    
    def test_data_value_to_dict_boolean(self):
        data_value = entity_pb2.EntityDataValue(boolean=True)
        result = data_value_to_dict("test",data_value)
        assert result == {"test":True}

    def test_data_value_to_dict_s3_file(self):
        data_value = entity_pb2.EntityDataValue(s3_file=data_type_pb2.S3File(bucket="bucket",key="key"))
        result = data_value_to_dict("test",data_value)
        assert result == {"test":"s3://bucket/key"}

    def test_data_value_to_dict_entity(self):
        data_value = entity_pb2.EntityDataValue(entity=entity_pb2.Entity(unique_id="111"))
        result = data_value_to_dict("test",data_value)
        assert result == {"test_unique_id":"111"}



if __name__ == '__main__':
    unittest.main()