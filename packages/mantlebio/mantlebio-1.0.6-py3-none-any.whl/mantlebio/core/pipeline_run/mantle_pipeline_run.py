
from abc import abstractmethod
import inspect
import os
from typing import Any, Dict, Iterable, Optional, Union
from mantlebio.core.dataset.client import _IDatasetClient
from mantlebio.core.dataset.mantle_dataset import _IDataset, MantleDataset
from mantlebio.core.pipeline_run.helpers import MantlePipelineRunKickoff, validate_pipeline_run_value
from mantlebio.core.session.mantle_session import _ISession
from mantlebio.core.storage.client import _IStorageClient
from mantlebio.exceptions import MantleAttributeError, MantleInvalidParameterError, MantleMissingParameterError, MantleProtoError
from mantlebio.helpers.decorators import deprecated
from pathlib import Path
from google.protobuf.message import DecodeError

from proto import data_type_pb2, entity_pb2, pipeline_pb2, pipeline_run_pb2


class _IPipelineRun:

    @abstractmethod
    def __init__(self, pipeline_run: Union[pipeline_run_pb2.PipelineRun, MantlePipelineRunKickoff], session: _ISession, storage_client: _IStorageClient, dataset_client: _IDatasetClient) -> None:
        raise NotImplementedError

    @abstractmethod
    def __getattr__(self, name):
        raise NotImplementedError

    @abstractmethod
    def _build_pipeline_run_value(self, value: Any) -> pipeline_pb2.PipelineRunValue:
        raise NotImplementedError

    @abstractmethod
    def _build_pipeline_data(self, pipeline_data: Dict[str, Any], data_class) -> Any:
        raise NotImplementedError

    @abstractmethod
    def _build_pipeline_output(self, pipeline_outputs: Dict[str, Any]) -> pipeline_run_pb2.PipelineOutputs:
        raise NotImplementedError

    @abstractmethod
    def _build_pipeline_input(self, pipeline_inputs: Dict[str, Any]) -> pipeline_run_pb2.PipelineInputs:
        raise NotImplementedError

    @abstractmethod
    def _build_pipeline_kickoff(
        self,
        pipeline_id: str,
        pipeline_version: str = "",
        external: bool = False,
        inputs: Optional[Dict] = None

    ) -> pipeline_run_pb2.PipelineKickOff:
        raise NotImplementedError

    @abstractmethod
    def add_input(self, key: str, value: Any):
        raise NotImplementedError

    @abstractmethod
    def add_output(self, key: str, value: Any):
        raise NotImplementedError

    @abstractmethod
    def update_status(self, status: str):
        raise NotImplementedError

    @abstractmethod
    def get_input(self, key: str) -> Union[pipeline_pb2.PipelineRunValue, _IDataset]:
        raise NotImplementedError

    @abstractmethod
    def get_output(self, key: str) -> Union[pipeline_pb2.PipelineRunValue, _IDataset]:
        raise NotImplementedError

    @deprecated("2.0.0", "use get_input() instead")
    @abstractmethod
    def pull_input(self, key: str) -> pipeline_pb2.PipelineRunValue:
        raise NotImplementedError

    @deprecated("2.0.0", "use get_output() instead")
    @abstractmethod
    def pull_output(self, key: str) -> pipeline_pb2.PipelineRunValue:
        raise NotImplementedError

    @abstractmethod
    def get_id(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_unique_id(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_pipeline_id(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_pipeline_version(self) -> str:
        raise NotImplementedError

    @deprecated("2.0.0", "use add_input() instead")
    @abstractmethod
    def post_input(self, key: str, value: Any):
        raise NotImplementedError

    @deprecated("2.0.0", "use add_output() instead")
    @abstractmethod
    def post_output(self, key: str, value: Any):
        raise NotImplementedError

    @deprecated("2.0.0", "use get_input_dataset_list() instead")
    @abstractmethod
    def pull_entities_input(self, key: str) -> Union[Iterable[_IDataset], None]:
        raise NotImplementedError

    @deprecated("2.0.0", "use get_input_dataset() instead")
    @abstractmethod
    def pull_entity_input(self, key: str) -> Union[_IDataset, None]:
        raise NotImplementedError

    @deprecated("2.0.0", "use get_input_dataset_list() instead")
    @abstractmethod
    def get_input_entities(self, key: str) -> Iterable[_IDataset]:
        raise NotImplementedError

    @deprecated("2.0.0", "use get_output_dataset_list() instead")
    @abstractmethod
    def get_output_entities(self, key: str) -> Iterable[_IDataset]:
        raise NotImplementedError

    @abstractmethod
    def get_output_dataset_list(self, key: str) -> Iterable[_IDataset]:
        raise NotImplementedError

    @abstractmethod
    def get_input_entity(self, key: str) -> _IDataset:
        raise NotImplementedError

    @abstractmethod
    def get_input_dataset(self, key: str) -> _IDataset:
        raise NotImplementedError

    @abstractmethod
    def get_input_dataset_list(self, key: str) -> Iterable[_IDataset]:
        raise NotImplementedError

    @abstractmethod
    def get_s3_input(self, key: str, local_path: str) -> None:
        raise NotImplementedError

    @deprecated("2.0.0", "use add_output() instead")
    @abstractmethod
    def push_output(self, key: str, value: Any):
        raise NotImplementedError

    @abstractmethod
    def add_s3_output(self, url: str, output_key: str):
        raise NotImplementedError

    @abstractmethod
    def add_file_output(self, output_key: str, local_path: str):
        raise NotImplementedError

    @abstractmethod
    def add_folder_output(self, output_key: str, local_path_str: str):
        raise NotImplementedError

    @deprecated("2.0.0", "use add_dataset_output() instead")
    @abstractmethod
    def add_entity_output(self, output_key: str, entity: _IDataset):
        raise NotImplementedError

    @abstractmethod
    def add_dataset_output(self, output_key: str, dataset: _IDataset):
        raise NotImplementedError

    @deprecated("2.0.0", "use get_s3_input() instead")
    @abstractmethod
    def pull_s3_input(self, key: str, local_path: str) -> None:
        raise NotImplementedError

    @deprecated("2.0.0", "proto object is now wrapped by PipelineRun class")
    @property
    @abstractmethod
    def pipeline_run_pb2(self) -> pipeline_run_pb2.PipelineRun:
        raise NotImplementedError


class MantlePipelineRun(_IPipelineRun):
    '''
    MantlePipelineRun object for making requests to the Mantle API
    '''

    def __init__(self, pipeline_run: Union[pipeline_run_pb2.PipelineRun, MantlePipelineRunKickoff], session: _ISession, storage_client: _IStorageClient, dataset_client: _IDatasetClient) -> None:
        self._session = session
        self._storage_client = storage_client
        self._dataset_client = dataset_client

        if isinstance(pipeline_run, pipeline_run_pb2.PipelineRun):
            self._pipeline_run_instance = pipeline_run
            self._route_stem = f"/pipeline_run/{self._pipeline_run_instance.unique_id}/"
        else:
            pipeline_kickoff = self._build_pipeline_kickoff(
                pipeline_id=pipeline_run.pipeline_id,
                pipeline_version=pipeline_run.pipeline_version,
                external=pipeline_run.external,
                inputs=pipeline_run.inputs
            )

            res = self._session.make_request(
                "POST", f"/pipeline_run", data=pipeline_kickoff
            )

            if not res.ok:
                res.raise_for_status()

            try:
                new_pipeline_run_instance = pipeline_run_pb2.PipelineRun()
                new_pipeline_run_instance.ParseFromString(res.content)
                self._pipeline_run_instance = new_pipeline_run_instance
            except DecodeError as e:
                raise MantleProtoError(
                    res.content, pipeline_run_pb2.PipelineRun) from e

        self._route_stem = f"/pipeline_run/{self.unique_id}/"

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
        if hasattr(self._pipeline_run_instance, name):
            attr = getattr(self._pipeline_run_instance, name)
            if inspect.ismethod(attr):
                return self._wrap_method(attr)
            return attr
        raise MantleAttributeError(
            f"'{type(self._pipeline_run_instance).__name__}' object has no attribute '{name}'")

    def _build_pipeline_run_value(self, value: Any) -> pipeline_pb2.PipelineRunValue:
        one_of_kwarg = validate_pipeline_run_value(value=value)
        return pipeline_pb2.PipelineRunValue(**one_of_kwarg)

    def _build_pipeline_data(self, pipeline_data: Dict[str, Any], data_class) -> Any:
        """
        Generic function to build pipeline data.

        :param pipeline_data: Dictionary of pipeline data.
        :param data_class: The protobuf class for either PipelineOutputs or PipelineInputs.
        :return: An instance of data_class with populated data.
        """
        pipeline_args = {}
        for key, val in pipeline_data.items():
            if not isinstance(key, str):
                raise MantleInvalidParameterError(
                    "Pipeline keys must be strings.")
            pipeline_args[key] = self._build_pipeline_run_value(val)
        return data_class(data=pipeline_args)

    def _build_pipeline_output(self, pipeline_outputs: Dict[str, Any]) -> pipeline_run_pb2.PipelineOutputs:
        """
        Build a PipelineOutputs object from a dictionary of pipeline outputs.

        :param pipeline_outputs: Dictionary of pipeline output data.
        :return: PipelineOutputs protobuf object.
        """
        return self._build_pipeline_data(pipeline_outputs, pipeline_run_pb2.PipelineOutputs)

    def _build_pipeline_input(self, pipeline_inputs: Dict[str, Any]) -> pipeline_run_pb2.PipelineInputs:
        """
        Build a PipelineInputs object from a dictionary of pipeline inputs.

        :param pipeline_inputs: Dictionary of pipeline input data.
        :return: PipelineInputs protobuf object.
        """
        return self._build_pipeline_data(pipeline_inputs, pipeline_run_pb2.PipelineInputs)

    def _build_pipeline_kickoff(
        self,
        pipeline_id: str,
        pipeline_version: str = "",
        external: bool = False,
        inputs: Optional[Dict] = None

    ) -> pipeline_run_pb2.PipelineKickOff:
        pipeline_inputs = self._build_pipeline_input(
            pipeline_inputs=inputs or {})
        return pipeline_run_pb2.PipelineKickOff(pipeline_id=pipeline_id, pipeline_version=pipeline_version, external=external, inputs=pipeline_inputs)

    # TODO(https://mantlebio.atlassian.net/browse/ME-383) support adding new dataset inputs to pipeline
    def add_input(self, key: str, value: Any):
        """Add an input to the pipeline run

        Args:
            key (str): Input key
            value (Any): Input value

        Returns:
            PipelineRun: PipelineRun object

        Examples:
            >>> import mantlebio
            >>> mantle = mantlebio.MantleClient()
            >>> pipeline_run = mantle.pipeline_run.get("pipeline_run_id")
            >>> pipeline_run.add_input("input_key", "input_value")
        """
        if isinstance(value, _IDataset):
            value = value.to_proto()
        prv = self._build_pipeline_run_value(value=value)
        res = self._session.make_request(
            "POST", self._route_stem + f'input/{key}', data=prv)

        if not res.ok:
            res.raise_for_status()

        try:
            new_pipeline_run_instance = pipeline_run_pb2.PipelineRun()
            new_pipeline_run_instance.ParseFromString(res.content)
            if isinstance(value, data_type_pb2.FileUpload):
                s3_file_upload_proto = new_pipeline_run_instance.inputs.data[key].s3_file
                if s3_file_upload_proto is None:
                    raise MantleMissingParameterError(
                        f"Property {key} is missing an S3 file.")
                upload_prefix = s3_file_upload_proto.key
                if not upload_prefix:
                    raise MantleMissingParameterError(
                        f"Property {key} is missing an S3 file key.")
                self._storage_client.upload(
                    prv.file_upload.filename, upload_prefix)
        except DecodeError as e:
            raise MantleProtoError(
                res.content, pipeline_run_pb2.PipelineRun) from e

        self._pipeline_run_instance.MergeFrom(new_pipeline_run_instance)

    def add_output(self, key: str, value: Any):
        """Add an output to the pipeline run

        Args:
            key (str): Output key
            value (Any): Output value

        Returns:
            PipelineRun: PipelineRun object

        Examples:
            >>> import mantlebio
            >>> mantle = mantlebio.MantleClient()
            >>> pipeline_run = mantle.pipeline_run.get("pipeline_run_id")
            >>> pipeline_run.add_output("output_key", "output_value")
        """
        if isinstance(value, _IDataset):
            value = value.to_proto()
        prv = self._build_pipeline_run_value(value=value)
        res = self._session.make_request(
            "POST", self._route_stem + f'output/{key}', data=prv)

        if not res.ok:
            res.raise_for_status()

        try:
            new_pipeline_run_instance = pipeline_run_pb2.PipelineRun()
            new_pipeline_run_instance.ParseFromString(res.content)
            new_pipeline_run_outputs = new_pipeline_run_instance.outputs
            if isinstance(value, data_type_pb2.FileUpload):
                s3_file_upload_proto = new_pipeline_run_outputs.data[key].s3_file
                if s3_file_upload_proto is None:
                    raise MantleMissingParameterError(
                        f"Property {key} is missing an S3 file.")
                upload_prefix = s3_file_upload_proto.key
                if not upload_prefix:
                    raise MantleMissingParameterError(
                        f"Property {key} is missing an S3 file key.")
                file_path = prv.file_upload.filename
                self._storage_client.upload(file_path, upload_prefix)
            self._pipeline_run_instance.MergeFrom(new_pipeline_run_instance)
        except DecodeError as e:
            raise MantleProtoError(
                res.content, pipeline_run_pb2.PipelineRun) from e

        self._pipeline_run_instance.MergeFrom(new_pipeline_run_instance)

    def update_status(self, status: str):
        """Update the status of a Pipeline Run

        Args:
            status (str): Pipeline Status

        Returns:
            PipelineRun: PipelineRun object

        Examples:
            >>> import mantlebio
            >>> mantle = mantlebio.MantleClient()
            >>> pipeline_run = mantle.pipeline_run.get("pipeline_run_id")
            >>> pipeline_run.update_status("COMPLETED")
        """
        status_req = pipeline_run_pb2.PipelineStatusUpdateRequest(
            status=status)
        res = self._session.make_request(
            "PATCH", f"{self._route_stem}status", data=status_req)
        pipeline_run_obj_pb2 = pipeline_run_pb2.PipelineRun()

        try:
            pipeline_run_obj_pb2.ParseFromString(res.content)
        except DecodeError as e:
            raise MantleProtoError(
                res.content, pipeline_run_pb2.PipelineRun) from e

        self._pipeline_run_instance.MergeFrom(pipeline_run_obj_pb2)

    def get_input(self, key: str) -> Union[pipeline_pb2.PipelineRunValue, _IDataset]:
        """Get an input from the pipeline run

        Args:
            key (str): Input key

        Returns:
            PipelineRunValue: PipelineRunValue object

        Examples:
            >>> import mantlebio
            >>> mantle = mantlebio.MantleClient()
            >>> pipeline_run = mantle.pipeline_run.get("pipeline_run_id")
            >>> pipeline_run.get_input("input_key")
        """

        try:
            value = self._pipeline_run_instance.inputs.data[key]
            if value.WhichOneof("value") == "entity" and value.entity.unique_id != "":
                return MantleDataset(dataset_input=value.entity, session=self._session, storage_client=self._storage_client)
            return value
        except KeyError as k:
            raise MantleAttributeError(
                f"Input {key} not found in pipeline run.") from k

    def get_output(self, key: str) -> Union[pipeline_pb2.PipelineRunValue, _IDataset]:
        """Get an output from the pipeline run

        Args:
            key (str): Output key

        Returns:
            PipelineRunValue: PipelineRunValue object

        Examples:
            >>> import mantlebio
            >>> mantle = mantlebio.MantleClient()
            >>> pipeline_run = mantle.pipeline_run.get("pipeline_run_id")
            >>> pipeline_run.get_output("output_key")

        """
        try:
            value = self._pipeline_run_instance.outputs.data[key]
            if value.WhichOneof("value") == "entity" and value.entity.unique_id != "":
                return MantleDataset(dataset_input=value.entity, session=self._session, storage_client=self._storage_client)
            return value
        except KeyError as k:
            raise MantleAttributeError(
                f"Output {key} not found in pipeline run.") from k

    @deprecated("2.0.0", "use get_input() instead")
    def pull_input(self, key: str) -> pipeline_pb2.PipelineRunValue:
        """
        Pull a pipeline input from the pipeline run input
        """
        return self.get_input(key=key)

    @deprecated("2.0.0", "use get_output() instead")
    def pull_output(self, key: str) -> pipeline_pb2.PipelineRunValue:
        """
        Pull a pipeline output from the pipeline run output
        """
        return self.get_output(key=key)

    @deprecated("2.0.0", "use .id instead")
    def get_id(self) -> str:
        return self._pipeline_run_instance.id

    @deprecated("2.0.0", "use .unique_id instead")
    def get_unique_id(self) -> str:
        return self._pipeline_run_instance.unique_id

    @deprecated("2.0.0", "use .pipeline_id instead")
    def get_pipeline_id(self) -> str:
        return self._pipeline_run_instance.pipeline_id

    @deprecated("2.0.0", "use .pipeline_version instead")
    def get_pipeline_version(self) -> str:
        return self._pipeline_run_instance.pipeline_version

    @deprecated("2.0.0", "use add_input() instead")
    def post_input(self, key: str, value: Any):
        self.add_input(key, value)

    @deprecated("2.0.0", "use add_output() instead")
    def post_output(self, key: str, value: Any):
        self.add_output(key, value)

    @deprecated("2.0.0", "use get_input_dataset_list() instead")
    def get_input_entities(self, key: str) -> Iterable[_IDataset]:
        return self.get_input_dataset_list(key=key)

    def get_input_dataset_list(self, key: str) -> Iterable[_IDataset]:
        """
        Get a list of datasets from the pipeline run that belong to a given input key

        Args:
            key (str): Input key

        Returns:
            list: List of Dataset objects


        Examples:
            >>> import mantlebio
            >>> mantle = mantlebio.MantleClient()
            >>> pipeline_run = mantle.pipeline_run.get("pipeline_run_id")
            >>> dataset_list = pipeline_run.get_input_dataset_list("input_key")
            >>> # Returns a list of Dataset objects
            >>> for dataset in dataset_list:
            >>>     print(dataset.get_id())

        """
        res = self.get_input(key=key)
        out = []
        if res.entity.unique_id != "":
            dataset = self._dataset_client.get(id=res.entity.unique_id)
            out.append(dataset)
            return out
        for proto_obj in res.entities.entities:
            dataset = self._dataset_client.get(id=proto_obj.unique_id)
            out.append(dataset)
        return out

    @deprecated("2.0.0", "use get_output_dataset_list() instead")
    def get_output_entities(self, key: str) -> Iterable[_IDataset]:
        return self.get_output_dataset_list(key=key)

    def get_output_dataset_list(self, key: str) -> Iterable[_IDataset]:
        """
        Get a list of datasets from the pipeline run that belong to a given output key

        Args:
            key (str): Output key

        Returns:
            list: List of Dataset objects

        Examples:
            >>> import mantlebio
            >>> mantle = mantlebio.MantleClient()
            >>> pipeline_run = mantle.pipeline_run.get("pipeline_run_id")
            >>> dataset_list = pipeline_run.get_output_dataset_list("output_key")
            >>> # Returns a list of Dataset objects
            >>> for dataset in dataset_list:
            >>>     print(dataset.get_id())

        """
        res = self.get_output(key=key)
        out = []
        if res.entity.unique_id != "":
            dataset = self._dataset_client.get(id=res.entity.unique_id)
            out.append(dataset)
            return out
        for proto_obj in res.entities.entities:
            dataset = self._dataset_client.get(id=proto_obj.unique_id)
            out.append(dataset)
        return out

    @deprecated("2.0.0", "use get_input_dataset_list() instead")
    def pull_entities_input(self, key: str) -> Union[Iterable[_IDataset], None]:
        self.get_input_dataset_list(key=key)

    @deprecated("2.0.0", "use get_input_dataset() instead")
    def pull_entity_input(self, key: str) -> Union[_IDataset, None]:
        self.get_input_dataset(key=key)

    @deprecated("2.0.0", "use get_input_dataset() instead")
    def get_input_entity(self, key: str) -> _IDataset:
        return self.get_input_dataset(key=key)

    def get_input_dataset(self, key: str) -> _IDataset:
        """
        Get a dataset from the pipeline run from an input key

        Args:
            key (str): Input key

        Returns:
            Dataset: Dataset object

        Examples:
            >>> import mantlebio
            >>> mantle = mantlebio.MantleClient()
            >>> pipeline_run = mantle.pipeline_run.get("pipeline_run_id")
            >>> dataset = pipeline_run.get_input_dataset("input_key")
        """
        res = self.get_input(key=key)

        if res.entity.unique_id == "":
            raise MantleMissingParameterError(
                f"Property {key} is missing a dataset.")

        dataset = self._dataset_client.get(id=res.entity.unique_id)
        return dataset

    @deprecated("2.0.0", "use get_s3_input() instead")
    def pull_s3_input(self, key: str, local_path: str) -> None:
        self.get_s3_input(key=key, local_path=local_path)

    def get_s3_input(self, key: str, local_path: str) -> None:
        """
        Pull a pipeline input from the pipeline run input

        Args:
            key (str): Input key
            local_path (str): Local path to save the S3 file

        Returns:
            None

        Side Effects:
            Downloads the S3 file to the local path specified

        Examples:
            >>> import mantlebio
            >>> mantle = mantlebio.MantleClient()
            >>> pipeline_run = mantle.pipeline_run.get("pipeline_run_id")
            >>> pipeline_run.get_s3_input("input_key", "path/to/local/file")
        """
        value = self.get_input(key=key)

        if value.s3_file is None:
            raise MantleMissingParameterError(
                f"Property {key} is missing an S3 file.")

        if value.s3_file.bucket is None:
            raise MantleMissingParameterError(
                f"Property {key} is missing an S3 file bucket.")

        if value.s3_file.key is None:
            raise MantleMissingParameterError(
                f"Property {key} is missing an S3 file key.")

        self._storage_client.download(
            value.s3_file.bucket, value.s3_file.key, local_path)

    @deprecated("2.0.0", "use add_output() instead")
    def push_output(self, key: str, value: Any):
        """Add an output to the pipeline run

        Args:
            key(str): Output key
            value(Any): Output value

        Returns:
            PipelineRun: PipelineRun proto object

        """
        return self.add_output(key, value)

    def add_s3_output(self, url: str, output_key: str):
        '''
        Add an S3 output to the pipeline run

        Args:
            url (str): S3 URL to the file format: s3://bucket/key
            output_key (str): Output key

        Returns:
            None

        Examples:
            >>> import mantlebio
            >>> mantle = mantlebio.MantleClient()
            >>> pipeline_run = mantle.pipeline_run.get("pipeline_run_id")
            >>> pipeline_run.add_s3_output("s3://bucket/key", "output_key")
        '''
        bucket = url.split('/')[2]
        s3_key = '/'.join(url.split('/')[3:])

        s3_data_value = data_type_pb2.S3File(bucket=bucket, key=s3_key)
        self.add_output(key=output_key, value=s3_data_value)

    def add_file_output(self, output_key: str, local_path: str):
        '''
        Add a file output to the pipeline run

        Args:
            output_key (str): Output key
            local_path (str): Local path to the file

        Returns:
            None

        Examples:
            >>> import mantlebio
            >>> mantle = mantlebio.MantleClient()
            >>> pipeline_run = mantle.pipeline_run.get("pipeline_run_id")
            >>> pipeline_run.add_file_output("output_key", "path/to/local/file")
        '''
        file_upload = data_type_pb2.FileUpload(filename=local_path)

        self.add_output(output_key, file_upload)

    def add_folder_output(self, output_key: str, local_path_str: str):
        '''
        Add a folder output to the pipeline run

        Args:
            output_key (str): Output key
            local_path_str (str): Local path to the folder

        Returns:
            None

        Examples:
            >>> import mantlebio
            >>> mantle = mantlebio.MantleClient()
            >>> pipeline_run = mantle.pipeline_run.get("pipeline_run_id")
            >>> pipeline_run.add_folder_output("output_key", "path/to/local/folder")
        '''
        local_path = Path(local_path_str)
        if not local_path.is_dir():
            raise MantleInvalidParameterError(
                "The specified path is not a directory.")

        upload_file = data_type_pb2.FileUpload(
            filename=local_path_str
        )

        self.add_output(output_key, upload_file)

    @deprecated("2.0.0", "use add_dataset_output() instead")
    def add_entity_output(self, output_key: str, entity: _IDataset):
        # TODO(https://mantlebio.atlassian.net/browse/ME-383)
        self.add_output(output_key, entity_pb2.Entity(
            unique_id=entity.unique_id))

    @property
    def pipeline_run_pb2(self) -> pipeline_run_pb2.PipelineRun:
        return self._pipeline_run_instance
