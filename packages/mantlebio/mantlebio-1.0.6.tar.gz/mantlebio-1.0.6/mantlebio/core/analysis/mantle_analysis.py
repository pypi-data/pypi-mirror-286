import inspect
from typing import Any
from mantlebio.core.analysis.helpers import (
    unmarshall_analysis_proto,
    validate_analysis_value
)
from mantlebio.core.dataset.client import _IDatasetClient
from mantlebio.core.dataset.mantle_dataset import _IDataset, MantleDataset
from mantlebio.core.session.mantle_session import _ISession
from mantlebio.core.storage.client import _IStorageClient

from mantlebio.exceptions import MantleAttributeError, MantleInvalidParameterError
from mantlebio.helpers.decorators import deprecated
from proto import analysis_pb2, data_type_pb2, entity_pb2
from mantlebio.types.response.response_item import ResponseItem


class _IAnalysis(ResponseItem):
    """Wrapper for Analysis proto object with functions that extend the functionality of the proto object"""

    def __init__(self, analysis: analysis_pb2.Analysis, session: _ISession, storage_client: _IStorageClient, dataset_client: _IDatasetClient) -> None:
        '''
        Initialize the MantleAnalysis object.

        Args:
            analysis (analysis_pb2.Analysis): The Analysis proto object
            session (_ISession): MantleSession object for making calls to the mantle api
            storage_client (_IStorageClient): Storage client for uploading files
            dataset_client (_IDatasetClient): Dataset client for interacting with datasets
        '''
        raise NotImplementedError

    def add_file_input(self, input_key: str, local_path: str):
        """
        Add a file input to the MantleAnalysis object.

        Args:
            input_key (str): The key of the input.
            local_path (str): The local path of the file.
        """
        raise NotImplementedError

    def add_file_output(self, output_key: str, local_path: str):
        """
        Add a file output to the MantleAnalysis object.

        Args:
            output_key (str): The key of the output.
            local_path (str): The local path of the file.
        """
        raise NotImplementedError

    def add_input(self, input_key: str, val: Any, force: bool = False):
        """
        Add an input to the MantleAnalysis object.

        Args:
            input_key (str): The key of the input.
            val (Any): The value of the input.
        """
        raise NotImplementedError

    def get_input(self, key: str):
        """
        Get the value of an input.

        Args:
            key (str): The key of the input.

        Returns:
            Any: The value of the input.
        """
        raise NotImplementedError

    def get_output(self, key: str):
        """
        Get the value of an output.

        Args:
            key (str): The key of the output.

        Returns:
            Any: The value of the output.
        """
        raise NotImplementedError

    def add_output(self, output_key: str, val: Any, force: bool = False):
        """
        Add an output to the MantleAnalysis object.

        Args:
            output_key (str): The key of the output.
            val (Any): The value of the output.
        """
        raise NotImplementedError

    @deprecated("2.0.0", "Use get_output instead.")
    def pull_entity(self, key: str, entity_id: str) -> _IDataset:
        """
        Pull a dataset from the analysis input.

        Args:
            key (str): The key of the input.
            entity_id (str): The ID of the dataset.

        Returns:
            _IDataset: The pulled dataset.
        """
        raise NotImplementedError


class MantleAnalysis(_IAnalysis):
    """Wrapper for Analysis proto object with functions that extend the functionality of the proto object"""

    def __init__(self, analysis: analysis_pb2.Analysis, session: _ISession, storage_client: _IStorageClient, dataset_client: _IDatasetClient) -> None:
        '''
        Args:
            analysis (analysis_pb2.Analysis): The Analysis proto object
            session (_ISession): MantleSession object for making calls to the mantle api
            storage_client (_IStorageClient): Storage client for uploading files
            dataset_client (_IDatasetClient): Dataset client for interacting with datasets
        '''
        self._session = session
        self._storage_client = storage_client
        self._name = ""
        self._inputs = analysis.inputs.data
        self._outputs = analysis.outputs.data
        self._dataset_client = dataset_client
        self._analysis_instance = analysis  # the proto object

    def _wrap_method(self, method):
        def wrapper(*args, **kwargs):
            return method(*args, **kwargs)
        return wrapper

    def __getattr__(self, name):
        # First, check if the object itself has the property
        # TODO: this should be removed when we deprecate the proto property accessors
        try:
            return super().__getattribute__(name)
        except AttributeError:
            pass

        # Dynamically route attribute access to the protobuf object
        if hasattr(self._analysis_instance, name):
            attr = getattr(self._analysis_instance, name)
            if inspect.ismethod(attr):
                return self._wrap_method(attr)
            return attr
        raise MantleAttributeError(
            f"'{type(self._analysis_instance).__name__}' object has no attribute '{name}'")

    def add_file_input(self, input_key: str, local_path: str):
        """
        Add a file input to the MantleAnalysis object.

        Args:
            input_key (str): The key of the input.
            local_path (str): The local path of the file.

        Examples:
            >>> import mantlebio
            >>> mantle = mantlebio.MantleClient()
            >>> analysis = mantle.analysis.get("analysis_id")
            >>> analysis.add_file_input("input_key", "local/path/to/file")
        """
        new_s3_file_pb2 = data_type_pb2.FileUpload(
            filename=local_path
        )

        self.add_input(input_key, new_s3_file_pb2)

    def add_file_output(self, output_key: str, local_path: str):
        """
        Add a file output to the MantleAnalysis object.

        Args:
            output_key (str): The key of the output.
            local_path (str): The local path of the file.

        Examples:
            >>> import mantlebio
            >>> mantle = mantlebio.MantleClient()
            >>> analysis = mantle.analysis.get("analysis_id")
            >>> analysis.add_file_output("output_key", "local/path/to/file")
        """
        new_s3_file_pb2 = data_type_pb2.FileUpload(
            filename=local_path
        )
        self.add_output(output_key, new_s3_file_pb2)

    def add_input(self, input_key: str, val: Any):
        """
        Add an input to the MantleAnalysis object.

        Args:
            input_key (str): The key of the input.
            val (Any): The value of the input.

        Examples:
            >>> import mantlebio
            >>> mantle = mantlebio.MantleClient()
            >>> analysis = mantle.analysis.get("analysis_id")
            >>> analysis.add_input("input_key", "input_value")
        """
        if self._inputs.get(input_key):
            raise MantleInvalidParameterError(
                f"Input '{input_key}' already exists"
            )

        if isinstance(val, _IDataset):
            val = val.to_proto()
        analysis_value_args = validate_analysis_value(val)

        self._inputs.get_or_create(input_key).CopyFrom(analysis_pb2.AnalysisValue(
            **analysis_value_args))
        self._push_input(input_key)

    def get_input(self, key: str):
        """
        Get the value of an input.

        Args:
            key (str): The key of the input.

        Returns:
            Any: The value of the input.

        Examples:
            >>> import mantlebio
            >>> mantle = mantlebio.MantleClient()
            >>> analysis = mantle.analysis.get("analysis_id")
            >>> input_value = analysis.get_input("input_key")
        """
        input = self._inputs[key]
        value_type = input.WhichOneof('value')
        if value_type == "entity":
            return MantleDataset(input.entity, self._session, self._dataset_client)
        return input.__getattribute__(value_type)

    def get_output(self, key: str):
        """
        Get the value of an output.

        Args:
            key (str): The key of the output.

        Returns:
            Any: The value of the output.

        Examples:
            >>> import mantlebio
            >>> mantle = mantlebio.MantleClient()
            >>> analysis = mantle.analysis.get("analysis_id")
            >>> output_value = analysis.get_output("output_key")
        """
        output = self._outputs[key]
        value_type = output.WhichOneof('value')
        if value_type == "entity":
            return MantleDataset(output.entity, self._session, self._dataset_client)
        return output.__getattribute__(value_type)

    def add_output(self, output_key: str, val: Any, force: bool = False):
        """
        Add an output to the MantleAnalysis object.

        Args:
            output_key (str): The key of the output.
            val (Any): The value of the output.

        Examples:
            >>> import mantlebio
            >>> mantle = mantlebio.MantleClient()
            >>> analysis = mantle.analysis.get("analysis_id")
            >>> analysis.add_output("output_key", "output_value")
        """
        if self._outputs.get(output_key):
            raise MantleInvalidParameterError(
                f"Output '{output_key}' already exists"
            )

        if isinstance(val, _IDataset):
            val = val.to_proto()
        analysis_value_args = validate_analysis_value(val)
        self._outputs.get_or_create(output_key).CopyFrom(analysis_pb2.AnalysisValue(
            **analysis_value_args))
        self._push_output(output_key)

    def _push_output(self, key: str):
        """
        Push a value to the analysis output.

        Args:
            key (str): The key of the output.
        """
        if not self._outputs.get(key):
            raise KeyError(f"Output '{key}' not found.")

        field_label = self._outputs[key].WhichOneof('value')

        if field_label == "file_upload":
            file_upload_pb2_obj: data_type_pb2.FileUpload = self.get_output(
                key)

            if not file_upload_pb2_obj.filename:
                raise MantleInvalidParameterError(
                    "FileUpload object must have a filename attribute")

        if field_label == "entity":
            entity_pb2_obj: entity_pb2.Entity = self.get_output(key).to_proto()

            self._outputs[key].CopyFrom(
                analysis_pb2.AnalysisValue(entity=entity_pb2_obj))

        # update the analysis record with a new output
        analysis_resp = self._session.make_request(
            "POST", f"/analysis/{self.unique_id}/output/{key}",
            data=self._outputs[key]
        )

        if not analysis_resp.ok:
            analysis_resp.raise_for_status()

        analysis_pb2_obj = unmarshall_analysis_proto(
            proto_content=analysis_resp.content)

        self._analysis_instance = analysis_pb2_obj

        if field_label == "file_upload":
            s3_key = analysis_pb2_obj.outputs.data[key].s3_file.key
            new_s3_file_pb2 = self._storage_client.upload(
                path=file_upload_pb2_obj.filename, upload_key=s3_key)
            self._outputs[key].CopyFrom(
                analysis_pb2.AnalysisValue(s3_file=new_s3_file_pb2))
            self._analysis_instance.outputs.data[key].s3_file.CopyFrom(new_s3_file_pb2
                                                                       )

    def _push_input(self, key: str):
        """
        Push a value to the analysis input.

        Args:
            key (str): The key of the input.
        """
        if not self._inputs.get(key):
            raise KeyError(f"Input '{key}' not found.")

        field_label = self._inputs[key].WhichOneof('value')

        if field_label == "file_upload":
            file_upload_pb2_obj: data_type_pb2.FileUpload = self.get_input(key)

            if not file_upload_pb2_obj.filename:
                raise MantleInvalidParameterError(
                    "FileUpload object must have a filename attribute")

        if field_label == "entity":
            entity_pb2_obj: entity_pb2.Entity = self.get_input(key).to_proto()
            if not entity_pb2_obj.unique_id:
                raise ValueError(f"Cannot add entity that does not exist.")

            self._inputs[key].CopyFrom(
                analysis_pb2.AnalysisValue(entity=entity_pb2_obj))

        # once any file uploading has been completed,
        # update the analysis record with a new input
        analysis_resp = self._session.make_request(
            "POST", f"/analysis/{self.unique_id}/input/{key}",
            data=self._inputs[key]
        )

        if not analysis_resp.ok:
            analysis_resp.raise_for_status()

        analysis_pb2_obj = unmarshall_analysis_proto(
            proto_content=analysis_resp.content)
        self._analysis_instance = analysis_pb2_obj

        if field_label == "file_upload":

            s3_key = analysis_pb2_obj.inputs.data[key].s3_file.key
            new_s3_file_pb2 = self._storage_client.upload(
                path=file_upload_pb2_obj.filename, upload_key=s3_key)

            self._inputs[key].CopyFrom(
                analysis_pb2.AnalysisValue(s3_file=new_s3_file_pb2))

            self._analysis_instance.inputs.data[key].s3_file.CopyFrom(
                new_s3_file_pb2)
