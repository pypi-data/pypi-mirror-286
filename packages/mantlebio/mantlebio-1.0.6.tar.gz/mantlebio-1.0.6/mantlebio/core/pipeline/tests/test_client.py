import unittest
from unittest.mock import MagicMock
from mantlebio.core.pipeline.client import PipelineClient
from mantlebio.core.session.mantle_session import _ISession
from mantlebio.exceptions import MantleMissingParameterError
from proto import pipeline_pb2

class TestPipelineClient(unittest.TestCase):

    def setUp(self):
        self.session = MagicMock(spec=_ISession)
        self.client = PipelineClient(self.session)

    def test_get_pipeline(self):
        pipeline_id = "test_pipeline_id"
        pipeline_version = "1.0.0"

        pipeline_resp = MagicMock()
        pipeline_proto = pipeline_pb2.Pipeline()
        self.session.make_request.return_value = pipeline_resp
        pipeline_resp.content = pipeline_proto.SerializeToString()

        result = self.client.get_pipeline(pipeline_id, pipeline_version)

        self.assertEqual(result._pipeline_instance, pipeline_proto)

    def test_get_pipeline_no_version(self):
        pipeline_id = "test_pipeline_id"

        pipeline_resp = MagicMock()
        pipeline_proto = pipeline_pb2.Pipeline()
        self.session.make_request.return_value = pipeline_resp
        pipeline_resp.content = pipeline_proto.SerializeToString()

        result = self.client.get_pipeline(pipeline_id)

        self.assertEqual(result._pipeline_instance, pipeline_proto)

    def test_get_pipeline_missing_id(self):
        pipeline_id = ""

        with self.assertRaises(MantleMissingParameterError):
            self.client.get_pipeline(pipeline_id)

    def test_get(self):
        pipeline_id = "test_pipeline_id"
        pipeline_version = "1.0.0"

        pipeline_resp = MagicMock()
        pipeline_proto = pipeline_pb2.Pipeline()
        self.session.make_request.return_value = pipeline_resp
        pipeline_resp.content = pipeline_proto.SerializeToString()

        result = self.client.get(pipeline_id, pipeline_version)

        self.assertEqual(result._pipeline_instance, pipeline_proto)

    def test_get_no_version(self):
        pipeline_id = "test_pipeline_id"

        pipeline_resp = MagicMock()
        pipeline_proto = pipeline_pb2.Pipeline()
        self.session.make_request.return_value = pipeline_resp
        pipeline_resp.content = pipeline_proto.SerializeToString()

        result = self.client.get(pipeline_id)

        self.assertEqual(result._pipeline_instance, pipeline_proto)

    def test_get_missing_id(self):
        pipeline_id = ""

        with self.assertRaises(MantleMissingParameterError):
            self.client.get(pipeline_id)

if __name__ == '__main__':
    unittest.main()