import unittest
from unittest.mock import MagicMock
from mantlebio.core.analysis.mantle_analysis import MantleAnalysis
from mantlebio.core.dataset.client import _IDatasetClient
from mantlebio.core.dataset.mantle_dataset import MantleDataset
from mantlebio.core.session.helpers import MantleSessionResponse
from mantlebio.core.session.mantle_session import _ISession
from mantlebio.core.storage.client import _IStorageClient
from mantlebio.exceptions import MantleInvalidParameterError
from mantlebio.factories.mantle_session_response_factory import create_test_reponse
from proto import analysis_pb2, data_type_pb2, entity_pb2
from proto import data_type_pb2


class TestMantleAnalysis(unittest.TestCase):

    def setUp(self):
        self.session = MagicMock(_ISession)
        self.storage_client = MagicMock(spec=_IStorageClient)
        self.dataset_client = MagicMock(_IDatasetClient)
        self.analysis_proto = analysis_pb2.Analysis()
        self.analysis = MantleAnalysis(
            self.analysis_proto, self.session, self.storage_client, self.dataset_client)

    def test_add_file_input(self):
        test_s3_file = data_type_pb2.S3File(
            bucket="test_bucket", key="test_key")
        test_analysis_response_content = analysis_pb2.AnalysisResponse()
        test_mantle_response = create_test_reponse(
            status_code=200, content=test_analysis_response_content.SerializeToString())
        self.storage_client.upload.return_value = test_s3_file
        self.session.make_request.return_value = test_mantle_response
        self.analysis.add_file_input("input_key", "/path/to/file")
        self.assertEqual(len(self.analysis._inputs), 1)
        self.assertEqual(self.analysis._inputs["input_key"], analysis_pb2.AnalysisValue(
            s3_file=test_s3_file))

    def test_add_file_output(self):
        test_s3_file = data_type_pb2.S3File(
            bucket="test_bucket", key="test_key")
        test_analysis_response_content = analysis_pb2.AnalysisResponse()
        test_mantle_response = create_test_reponse(
            status_code=200, content=test_analysis_response_content.SerializeToString())
        self.storage_client.upload.return_value = test_s3_file
        self.session.make_request.return_value = test_mantle_response
        self.analysis.add_file_output("output_key", "/path/to/file")
        self.assertEqual(len(self.analysis._outputs), 1)
        self.assertEqual(self.analysis._outputs["output_key"], analysis_pb2.AnalysisValue(
            s3_file=test_s3_file))

    def test_add_input(self):
        test_analysis_response_content = analysis_pb2.AnalysisResponse()
        test_mantle_response = create_test_reponse(
            status_code=200, content=test_analysis_response_content.SerializeToString())
        self.session.make_request.return_value = test_mantle_response
        self.analysis.add_input("input_key", "input_value")
        self.assertEqual(len(self.analysis._inputs), 1)
        self.assertEqual(
            self.analysis._inputs["input_key"].string, "input_value")

    def test_add_dataset_input(self):
        test_analysis_response_content = analysis_pb2.AnalysisResponse()
        test_mantle_response = create_test_reponse(
            status_code=200, content=test_analysis_response_content.SerializeToString())
        self.session.make_request.return_value = test_mantle_response
        test_dataset = MantleDataset(dataset_input=entity_pb2.Entity(
            unique_id="test_id"), session=self.session, storage_client=self.storage_client)
        test_dataset_value = analysis_pb2.AnalysisValue(
            entity=test_dataset.to_proto())
        self.analysis.add_input("input_key", test_dataset)
        self.assertEqual(len(self.analysis._inputs), 1)
        self.assertEqual(
            self.analysis._inputs["input_key"], test_dataset_value)

    def test_get_input(self):
        stringInput = analysis_pb2.AnalysisValue(string="input_value")
        self.analysis._inputs["input_key"].CopyFrom(stringInput)
        value = self.analysis.get_input("input_key")
        self.assertEqual(value, stringInput.string)

    def test_get_output(self):
        stringOutput = analysis_pb2.AnalysisValue(string="output_value")
        self.analysis._outputs["output_key"].CopyFrom(stringOutput)
        value = self.analysis.get_output("output_key")
        self.assertEqual(value, stringOutput.string)

    def test_add_output(self):
        test_analysis_response_content = analysis_pb2.AnalysisResponse()
        test_mantle_response = create_test_reponse(
            status_code=200, content=test_analysis_response_content.SerializeToString())
        self.session.make_request.return_value = test_mantle_response
        test_dataset = MantleDataset(dataset_input=entity_pb2.Entity(
            unique_id="test_id"), session=self.session, storage_client=self.storage_client)
        test_dataset_value = analysis_pb2.AnalysisValue(
            entity=test_dataset.to_proto())
        self.analysis.add_output("output_key", test_dataset)
        self.assertEqual(len(self.analysis._outputs), 1)
        self.assertEqual(
            self.analysis._outputs["output_key"], test_dataset_value)
        
    def test_add_input_already_exists(self):
        test_analysis_response_content = analysis_pb2.AnalysisResponse()
        test_mantle_response = create_test_reponse(
            status_code=200, content=test_analysis_response_content.SerializeToString())
        self.session.make_request.return_value = test_mantle_response
        self.analysis.add_input("input_key", "input_value")
        with self.assertRaises(MantleInvalidParameterError) as err:
            self.analysis.add_input("input_key", "input")

        self.assertEqual(
            str(err.exception), "Input 'input_key' already exists")

    def test_add_output_already_exists(self):
        test_analysis_response_content = analysis_pb2.AnalysisResponse()
        test_mantle_response = create_test_reponse(
            status_code=200, content=test_analysis_response_content.SerializeToString())
        self.session.make_request.return_value = test_mantle_response
        self.analysis.add_output("output_key", "output_value")
        with self.assertRaises(MantleInvalidParameterError) as err:
            self.analysis.add_output("output_key", "output")

        self.assertEqual(
            str(err.exception), "Output 'output_key' already exists")

if __name__ == '__main__':
    unittest.main()
