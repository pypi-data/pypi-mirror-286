import unittest
from unittest.mock import MagicMock
from mantlebio.core.dataset.client import DatasetClient
from mantlebio.core.dataset.mantle_dataset import MantleDataset
from mantlebio.core.session.mantle_session import _ISession
from mantlebio.core.storage.client import _IStorageClient
from mantlebio.exceptions import MantleApiError, MantleInvalidParameterError, MantleProtoError
from mantlebio.types.response.list_reponse import ListResponse
from proto import data_type_pb2, entity_pb2
from typing import Dict, Any, Optional, Iterable
from mantlebio.helpers.decorators import deprecated
from requests import HTTPError


class TestDatasetClient(unittest.TestCase):

    def setUp(self):
        self.session = MagicMock(spec=_ISession)
        self.storage_client = MagicMock(spec=_IStorageClient)
        self.client = DatasetClient(self.session, self.storage_client)

    def test_get(self):
        id = "test_id"
        dataset_resp = MagicMock()
        entity_pb2_obj = entity_pb2.Entity()
        self.session.make_request.return_value = dataset_resp
        dataset_resp.ok = True
        dataset_resp.content = entity_pb2_obj.SerializeToString()

        result = self.client.get(id)

        self.assertIsInstance(result, MantleDataset)
        self.assertEqual(result.to_proto(), entity_pb2_obj)

    def test_get_error(self):
        id = "test_id"
        dataset_resp = MagicMock()
        self.session.make_request.return_value = dataset_resp
        dataset_resp.ok = False
        dataset_resp.raise_for_status.side_effect = MantleApiError

        with self.assertRaises(MantleApiError):
            self.client.get(id)

    def test_get_entity(self):
        id = "test_id"
        entity_resp = MagicMock()
        entity_pb2_obj = entity_pb2.Entity()
        self.session.make_request.return_value = entity_resp
        entity_resp.ok = True
        entity_resp.content = entity_pb2_obj.SerializeToString()

        result = self.client.get_entity(id)

        self.assertIsInstance(result, MantleDataset)
        self.assertEqual(result.to_proto(), entity_pb2_obj)

    def test_get_entities(self):
        entity_list_resp = MagicMock()
        entity_list_pb2 = entity_pb2.EntityList()
        self.session.make_request.return_value = entity_list_resp
        entity_list_resp.ok = True
        entity_list_resp.content = entity_list_pb2.SerializeToString()

        result = self.client.get_entities()

        self.assertIsInstance(result, Iterable)
        self.assertEqual(len(list(result)), len(entity_list_pb2.entities))

    def test_get_entities_error(self):
        entity_list_resp = MagicMock()
        self.session.make_request.return_value = entity_list_resp
        entity_list_resp.ok = False
        entity_list_resp.raise_for_status.side_effect = MantleApiError

        with self.assertRaises(MantleApiError):
            self.client.get_entities()

    def test_create_cloud_dataset_error(self):
        dataset_type = "test_dataset_type"
        properties = {"prop1": {"string": "value1"},
                      "prop2": {"string": "value2"}}
        origin = entity_pb2.Origin()

        dataset_resp = MagicMock()
        dataset_resp.ok = False
        dataset_resp.raise_for_status.side_effect = MantleApiError
        self.session.make_request.return_value = dataset_resp

        with self.assertRaises(MantleApiError):
            self.client._create_cloud_dataset(dataset_type, properties, origin)

    def test_create_local_dataset_no_properties(self):
        dataset_type = "test_dataset_type"

        result = self.client._create_local_dataset(dataset_type=dataset_type)

        self.assertIsInstance(result, MantleDataset)
        self.assertEqual(result.to_proto().data_type.unique_id, dataset_type)

    def test_create(self):
        dataset_type = "test_dataset_type"
        properties = {"prop1": {"string": "value1"},
                      "prop2": {"string": "value2"}}
        local = True
        origin = entity_pb2.Origin()

        result = self.client.create(
            dataset_type=dataset_type, properties=properties, local=local, origin=origin)

        self.assertIsInstance(result, MantleDataset)
        self.assertEqual(result.to_proto().data_type.unique_id, dataset_type)

    @deprecated("2.0.0", "use create() instead.")
    def test_create_cloud_entity(self):
        entity_type = "test_entity_type"
        name = "test_name"
        properties = {"prop1": {"string": "value1"},
                      "prop2": {"string": "value2"}}

        entity_resp = MagicMock()
        entity_resp.ok = True
        entity_resp.content = entity_pb2.Entity(
            data_type=data_type_pb2.DataType(unique_id=entity_type)).SerializeToString()
        self.session.make_request.return_value = entity_resp

        result = self.client.create_cloud_entity(entity_type, properties)

        self.assertIsInstance(result, MantleDataset)

    def test_create_local_entity(self):
        entity_type = "test_entity_type"
        properties = {"prop1": {"string": "value1"},
                      "prop2": {"string": "value2"}}

        result = self.client.create_local_entity(entity_type, properties)

        self.assertIsInstance(result, MantleDataset)

    def test_create_empty_entity(self):
        result = self.client.create_empty_entity()

        self.assertIsInstance(result, MantleDataset)
        self.assertEqual(result.to_proto().data_type.unique_id, "")

    def test_create_entity_deprecated(self):
        entity_type = "test_entity_type"
        name = "test_name"
        properties = {"prop1": {"string": "value1"},
                      "prop2": {"string": "value2"}}

        with self.assertWarns(DeprecationWarning) as cm:
            result = self.client.create(
                name=name, entity_type=entity_type, properties=properties)

        self.assertEqual(
            cm.warning.args[0], f"entity_type parameter is deprecated and will be removed in version 2.0.0. Use dataset_type instead.")
        self.assertIsInstance(result, MantleDataset)
        self.assertEqual(result.to_proto().data_type.unique_id, entity_type)

    def test_list(self):
        query_params = {"param1": "value1", "param2": "value2"}
        dataset_list_resp = MagicMock()
        dataset_list_pb2 = entity_pb2.EntitiesResponse()
        self.session.make_request.return_value = dataset_list_resp
        dataset_list_resp.ok = True
        dataset_list_resp.content = dataset_list_pb2.SerializeToString()
        result = self.client.list(query_params)
        self.assertIsInstance(result, ListResponse)
        self.assertEqual(len(list(result)), len(dataset_list_pb2.entities))

    def test_list_error(self):
        query_params = {"param1": "value1", "param2": "value2"}
        dataset_list_resp = MagicMock()
        self.session.make_request.return_value = dataset_list_resp
        dataset_list_resp.ok = False
        dataset_list_resp.raise_for_status.side_effect = MantleApiError
        with self.assertRaises(MantleApiError):
            self.client.list(query_params)


if __name__ == '__main__':
    unittest.main()
