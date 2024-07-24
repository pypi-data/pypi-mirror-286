    
import unittest
from mantlebio.core.pipeline_run.helpers import MantlePipelineRunKickoff, validate_pipeline_run_value
from mantlebio.exceptions import MantleTypeError
from proto import analysis_pb2, data_type_pb2, entity_pb2, pipeline_pb2
from mantlebio.core.analysis.helpers import unmarshall_analysis_proto, validate_analysis_value

class TestAnalysisHelpers(unittest.TestCase):

    def test_unmarshall_analysis_proto(self):
        # Create a sample protobuf content
        analysis = analysis_pb2.Analysis()
        analysis.name = "Test Analysis"
        proto_content = analysis_pb2.AnalysisResponse()
        proto_content.analysis.CopyFrom(analysis)
        proto_content_bytes = proto_content.SerializeToString()

        # Call the function
        result = unmarshall_analysis_proto(proto_content_bytes)

        # Check if the unmarshalled object is correct
        self.assertEqual(result, analysis)
 
class TestValidateAnalysisValue(unittest.TestCase):

    def test_validate_analysis_value_with_dataset(self):
        value = entity_pb2.Entity()
        result = validate_analysis_value(value)
        self.assertEqual(result, {"entity": value})

    def test_validate_analysis_value_with_s3_file(self):
        value = data_type_pb2.S3File()
        result = validate_analysis_value(value)
        self.assertEqual(result, {"s3_file": value})

    def test_validate_analysis_value_with_file_upload(self):
        value = data_type_pb2.FileUpload()
        result = validate_analysis_value(value)
        self.assertEqual(result, {"file_upload": value})

    def test_validate_analysis_value_with_bool(self):
        value = True
        result = validate_analysis_value(value)
        self.assertEqual(result, {"bool": value})

    def test_validate_analysis_value_with_string(self):
        value = "test_string"
        result = validate_analysis_value(value)
        self.assertEqual(result, {"string": value})

    def test_validate_analysis_value_with_invalid_type(self):
        value = {"key": "value"}
        with self.assertRaises(MantleTypeError):
            validate_analysis_value(value)


if __name__ == '__main__':
    unittest.main()