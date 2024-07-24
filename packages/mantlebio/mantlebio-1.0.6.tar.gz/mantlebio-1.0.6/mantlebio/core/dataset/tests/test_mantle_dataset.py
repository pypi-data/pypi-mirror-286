import datetime
import unittest
from unittest.mock import MagicMock

import pandas as pd
from mantlebio.core.dataset.mantle_dataset import MantleDataset, MantleEntity
from mantlebio.exceptions import MantleInvalidParameterError, MantleMissingParameterError
from proto import common_pb2, data_type_pb2, entity_pb2

class TestMantleDataset(unittest.TestCase):

    def setUp(self):
        self.session = MagicMock()
        self.storage_client = MagicMock()

    def test_create_dataset_from_proto(self):
        proto_entity = entity_pb2.Entity()
        dataset = MantleDataset(proto_entity, self.session, self.storage_client)
        self.assertEqual(dataset._dataset_instance, proto_entity)

    def test_create_dataset_from_json(self):
        json_entity = {"name": "Test Dataset"}
        dataset = MantleDataset(json_entity, self.session, self.storage_client)
        self.assertEqual(dataset._dataset_instance.name, "Test Dataset")

    def test_to_proto(self):
        proto_entity = entity_pb2.Entity()
        dataset = MantleDataset(proto_entity, self.session, self.storage_client)
        self.assertEqual(dataset.to_proto(), proto_entity)

    def test_get_property_non_existing_key(self):
        proto_entity = entity_pb2.Entity()
        dataset = MantleDataset(proto_entity, self.session, self.storage_client)
        self.assertIsNone(dataset.get_property("key"))

    def test_set_name(self):
        proto_entity = entity_pb2.Entity()
        dataset = MantleDataset(proto_entity, self.session, self.storage_client)
        dataset.set_name("New Name")
        self.assertEqual(dataset._dataset_instance.name, "New Name")

    def test_to_dict(self):
        proto_entity = entity_pb2.Entity(
            unique_id="111",
            created_by=common_pb2.User(
                name="test_user",
            ),
            updated_by=common_pb2.User(
                name="test_user",
            ),
            props={
                "test_string": entity_pb2.EntityDataValue(
                    string="test"
                ),
                "test_int": entity_pb2.EntityDataValue(
                    int=1
                ),
                "test_float": entity_pb2.EntityDataValue(
                    double=1.0
                ),
                "test_bool": entity_pb2.EntityDataValue(
                    boolean=True
                ),
                "test_object": entity_pb2.EntityDataValue(
                    object=entity_pb2.EntityDataValue.DataObject(values = {})
                ),
                "test_dataset": entity_pb2.EntityDataValue(
                    entity=entity_pb2.Entity(
                        unique_id="123"
                    )
                )
            }
        )
        dataset = MantleDataset(proto_entity, self.session, self.storage_client)
        self.assertDictEqual(dataset.to_dict(), {
            "unique_id": "111",
            "created_by_user": "test_user",
            "updated_at": datetime.datetime(1970, 1, 1, 0, 0),
            "created_at": datetime.datetime(1970, 1, 1, 0, 0),
            "updated_by_user": "test_user",
            "test_string": "test",
            "test_int": 1,
            "test_float": 1.0,
            "test_bool": True,
            "test_object": "Unsupported Type",
            "test_dataset_unique_id": "123",
        })

    def test_to_series(self):
        proto_entity = entity_pb2.Entity(
            unique_id="111",
            created_by=common_pb2.User(
                name="test_user",
            ),
            updated_by=common_pb2.User(
                name="test_user",
            ),
            props={
                "test_string": entity_pb2.EntityDataValue(
                    string="test"
                ),
                "test_int": entity_pb2.EntityDataValue(
                    int=1
                ),
                "test_float": entity_pb2.EntityDataValue(
                    double=1.0
                ),
                "test_bool": entity_pb2.EntityDataValue(
                    boolean=True
                ),
                "test_object": entity_pb2.EntityDataValue(
                    object=entity_pb2.EntityDataValue.DataObject(values = {})
                ),
                "test_dataset": entity_pb2.EntityDataValue(
                    entity=entity_pb2.Entity(
                        unique_id="123"
                    )
                )
            }
        )
        dataset = MantleDataset(proto_entity, self.session, self.storage_client)
        expected_series = pd.Series({
            "unique_id": "111",
            "created_by_user": "test_user",
            "updated_at": datetime.datetime(1970, 1, 1, 0, 0),
            "created_at": datetime.datetime(1970, 1, 1, 0, 0),
            "updated_by_user": "test_user",
            "test_string": "test",
            "test_int": 1,
            "test_float": 1.0,
            "test_bool": True,
            "test_object": "Unsupported Type",
            "test_dataset_unique_id": "123",
        })

        pd.testing.assert_series_equal(dataset.to_series(), expected_series, check_like=True)

    def test_init_with_deprecated_keyword(self):
        proto_entity = entity_pb2.Entity()
        with self.assertWarns(DeprecationWarning) as cm:
            dataset = MantleDataset(entity_input=proto_entity, session=self.session, storage_client=self.storage_client, local=True)
        self.assertEqual(cm.warning.args[0], "entity_input parameter is deprecated and will be removed in version 2.0.0. Use dataset_input instead.")
        self.assertEqual(dataset._dataset_instance, proto_entity)

    def test_init_without_session(self):
        proto_entity = entity_pb2.Entity()
        with self.assertRaises(MantleMissingParameterError) as cm:
            MantleDataset(proto_entity, storage_client=self.storage_client)
        self.assertEqual(cm.exception.args[0], "Session object is required to create a dataset.")

    def test_init_without_storage(self):
        proto_entity = entity_pb2.Entity()
        with self.assertRaises(MantleMissingParameterError) as cm:
            MantleDataset(proto_entity, session=self.session)
        self.assertEqual(cm.exception.args[0], "Storage client object is required to create a dataset.")

    def test_entity_property(self):
        proto_entity = entity_pb2.Entity()
        dataset = MantleDataset(proto_entity, self.session, self.storage_client)
        self.assertIsInstance(dataset.entity, entity_pb2.Entity)

if __name__ == '__main__':
    unittest.main()