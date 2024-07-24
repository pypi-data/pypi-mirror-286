import unittest
from unittest.mock import MagicMock

from typing import Dict, Any, Optional
from mantlebio.core.analysis.client import AnalysisClient
from mantlebio.core.analysis.mantle_analysis import MantleAnalysis
from mantlebio.core.dataset.client import _IDatasetClient
from mantlebio.core.session.mantle_session import _ISession
from mantlebio.core.storage.client import _IStorageClient
from mantlebio.exceptions import MantleResourceNotFoundError
from proto import analysis_pb2


class TestAnalysisClient(unittest.TestCase):

    def setUp(self):
        self.session = MagicMock(spec=_ISession)
        self.storage_client = MagicMock(spec=_IStorageClient)
        self.dataset_client = MagicMock(spec=_IDatasetClient)
        self.client = AnalysisClient(
            self.session, self.storage_client, self.dataset_client)

    def test_new_analysis_with_inputs(self):
        name = "Test Analysis"
        inputs = {"input1": "value1", "input2": "value2"}

        analysis_resp = MagicMock()
        test_analysis_pb2 = analysis_pb2.Analysis()
        self.session.make_request.return_value = analysis_resp
        test_mantle_analysis = MantleAnalysis(
            test_analysis_pb2, self.session, self.storage_client, self.dataset_client)
        analysis_resp.content = test_analysis_pb2.SerializeToString()

        result = self.client.create(name, inputs)

        self.assertEqual(result._analysis_instance,
                         test_mantle_analysis._analysis_instance)

    def test_new_analysis_without_inputs(self):
        name = "Test Analysis"
        inputs = None

        analysis_resp = MagicMock()
        test_analysis_pb2 = analysis_pb2.Analysis()
        self.session.make_request.return_value = analysis_resp
        analysis_resp.content = test_analysis_pb2.SerializeToString()

        result = self.client.create(name, inputs)

        self.assertEqual(result._analysis_instance, test_analysis_pb2)

    def test_get(self):
        analysis_id = "test_analysis_id"

        analysis_resp = MagicMock()
        test_analysis_pb2 = analysis_pb2.Analysis()
        self.session.make_request.return_value = analysis_resp
        analysis_resp.content = test_analysis_pb2.SerializeToString()

        result = self.client.get(analysis_id)

        self.assertEqual(result._analysis_instance, test_analysis_pb2)


if __name__ == '__main__':
    unittest.main()
