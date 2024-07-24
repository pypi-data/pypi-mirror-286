import unittest
from unittest.mock import MagicMock
from mantlebio.core.dataset.mantle_dataset import MantleDataset, MantleEntity
from mantlebio.exceptions import MantleInvalidParameterError, MantleMissingParameterError
from proto import data_type_pb2, entity_pb2

class TestMantleEntity(unittest.TestCase):

    def setUp(self):
        self.session = MagicMock()
        self.storage_client = MagicMock()

    def test_create_entity_from_proto(self):
        proto_entity = entity_pb2.Entity()
        with self.assertWarns(DeprecationWarning) as cm:
            entity = MantleEntity(proto_entity, self.session, self.storage_client)
        self.assertEqual(str(cm.warnings[0].message), 'Class MantleEntity is deprecated and will be removed in version 2.0.0. use MantleDataset instead')
        self.assertEqual(entity._dataset_instance, proto_entity)

    def test_create_entity_from_json(self):
        json_entity = {"name": "Test Entity"}
        with self.assertWarns(DeprecationWarning) as cm:
            entity = MantleEntity(json_entity, self.session, self.storage_client)
        self.assertEqual(str(cm.warnings[0].message), 'Class MantleEntity is deprecated and will be removed in version 2.0.0. use MantleDataset instead')
        self.assertEqual(entity._dataset_instance.name, "Test Entity")

    def test_to_proto(self):
        proto_entity = entity_pb2.Entity()
        with self.assertWarns(DeprecationWarning) as cm:
            entity = MantleEntity(proto_entity, self.session, self.storage_client)
        self.assertEqual(str(cm.warnings[0].message), 'Class MantleEntity is deprecated and will be removed in version 2.0.0. use MantleDataset instead')
        self.assertEqual(entity.to_proto(), proto_entity)

    def test_get_property_non_existing_key(self):
        proto_entity = entity_pb2.Entity()
        with self.assertWarns(DeprecationWarning) as cm:
            entity = MantleEntity(proto_entity, self.session, self.storage_client)
        self.assertEqual(str(cm.warnings[0].message), 'Class MantleEntity is deprecated and will be removed in version 2.0.0. use MantleDataset instead')
        self.assertIsNone(entity.get_property("key"))

    def test_set_name(self):
        proto_entity = entity_pb2.Entity()
        with self.assertWarns(DeprecationWarning) as cm:
            entity = MantleEntity(proto_entity, self.session, self.storage_client)
            entity.set_name("New Name")
        self.assertEqual(str(cm.warnings[0].message), 'Class MantleEntity is deprecated and will be removed in version 2.0.0. use MantleDataset instead')
        self.assertEqual(entity._dataset_instance.name, "New Name")

if __name__ == '__main__':
    unittest.main()