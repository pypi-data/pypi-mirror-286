from abc import abstractmethod
import inspect
import os
from typing import Any, Dict, Optional, Union
import warnings

import pandas as pd
from pandas.core.api import Series as Series
from mantlebio.core.dataset.helpers import DatasetPropertiesBuilder, data_value_to_dict, dataset_params_from_json, validate_dataset_data_value
from mantlebio.core.session.mantle_session import _ISession
from mantlebio.core.storage.client import _IStorageClient
from mantlebio.exceptions import MantleAttributeError, MantleInvalidParameterError, MantleMissingParameterError, MantleProtoError
from mantlebio.helpers.decorators import deprecated
from mantlebio.types.response.response_item import ResponseItem
from proto import data_type_pb2
from proto import entity_pb2 as entity_proto
from pathlib import Path
from google.protobuf.message import Message, DecodeError


class _IDataset(ResponseItem):
    @abstractmethod
    def __init__(self, dataset_input: Union[entity_proto.Entity, Dict[str, Any]], session: _ISession, storage_client: _IStorageClient, local: bool = False, entity_input: Optional[Union[entity_proto.Entity, Dict[str, Any]]] = None):
        """ Initialize a Dataset. """
        raise NotImplementedError

    @abstractmethod
    def to_proto(self) -> entity_proto.Entity:
        """ Convert the dataset to a protocol buffer object. """
        raise NotImplementedError

    @abstractmethod
    def __str__(self) -> str:
        """ String representation of the dataset. """
        raise NotImplementedError

    @abstractmethod
    def __getattr__(self, name: str) -> Any:
        """ Get an attribute of the dataset. """
        raise NotImplementedError

    @abstractmethod
    def get_property(self, key: str) -> Optional[Message]:
        """ Get a property of the dataset. """
        raise NotImplementedError

    @abstractmethod
    def download_s3(self, key: str, local_path: str) -> None:
        """ Download a file from S3. """
        raise NotImplementedError

    @abstractmethod
    def upload_s3(self, key: str, local_path: str) -> None:
        """ Upload a file to S3. """
        raise NotImplementedError

    @abstractmethod
    def add_s3_file_property(self, key: str, bucket: str, s3_key: str) -> None:
        """ Add an S3 property to the dataset. """
        raise NotImplementedError

    @abstractmethod
    def set_name(self, name: str) -> None:
        """ Set the name of the dataset. """
        raise NotImplementedError

    @deprecated("2.0.0", "use set_property instead")
    @abstractmethod
    def set_data_type(self, data_type: str) -> None:
        """ Set the data type of the dataset. """
        raise NotImplementedError

    @abstractmethod
    def set_property(self, key: str, value: Any) -> None:
        """ Set a property of the dataset. """
        raise NotImplementedError

    @deprecated("2.0.0", "use create() instead")
    @abstractmethod
    def push(self) -> None:
        """ Push the dataset to the server. """
        raise NotImplementedError

    @deprecated("2.0.0", "use to_proto() instead")
    @property
    @abstractmethod
    def entity_pb2(self) -> entity_proto.Entity:
        """ Return the entity_pb2 object """
        raise NotImplementedError

    @deprecated("2.0.0", "use unique_id instead")
    @abstractmethod
    def get_id(self) -> str:
        """ Get the ID of the dataset. """
        raise NotImplementedError

    @property
    @deprecated("2.0.0", "in this version all datasets are reurned as _IDataset rather than PipelineRunValue or AnalysisValues no neet to get .entity")
    @abstractmethod
    def entity(self) -> entity_proto.Entity:
        """ Get the entity of the dataset. """
        raise NotImplementedError


class _IEntity(_IDataset):
    @deprecated("2.0.0", "use _IDataset instead")
    def __init__(self, entity_input: Union[entity_proto.Entity, Dict[str, Any]], session: _ISession, storage_client: _IStorageClient):
        """ Initialize a dataset. """
        raise NotImplementedError


class MantleDataset(_IDataset):

    def __init__(self, dataset_input: Optional[Union[entity_proto.Entity, Dict[str, Any]]] = None, session: _ISession = None, storage_client: _IStorageClient = None, local: bool = False, entity_input: Optional[Union[entity_proto.Entity, Dict[str, Any]]] = None):
        """
        Initialize a dataset with either a proto_entity_object or JSON data.

        This method allows for the creation of a dataset in two ways: 
        1. Automatically via a proto_entity_object typically received from clients or API requests.
        2. Manually via human-readable JSON represented as a python dictionary.

        Args:
            dataset_input (Union[entity_proto.Entity, Dict[str, Any]]): The dataset to be created.
            entity_input (Optional[entity_proto.Entity], optional): The entity to be created. Deprecated use dataset_input instead. Defaults to None.
            session (_ISession): The session object used for authentication.
            storage_client (_IStorageClient): The storage client object used for interacting with storage.
            local (bool, optional): Whether the dataset is local. Defaults to False.

        Raises:
            ValueError: if dataset input is not either a Dictionary or proto.
            MantleInvalidParameterError: if session or storage_client is not provided.
            MantleInvalidParameterError: if dataset_input is not provided.
        """
        # TODO: Reconsider the permissions and method for dataset creation to enhance security and robustness of the process.
        if not session:
            raise MantleMissingParameterError(
                "Session object is required to create a dataset.")

        if not storage_client:
            raise MantleMissingParameterError(
                "Storage client object is required to create a dataset.")

        if entity_input is not None:
            warnings.warn(f"entity_input parameter is deprecated and will be removed in version 2.0.0. Use dataset_input instead.",
                          category=DeprecationWarning, stacklevel=2)
            dataset_input = entity_input

        # Create dataset from proto_entity_object
        if isinstance(dataset_input, entity_proto.Entity):
            self._dataset_instance = dataset_input

        # Create dataset from JSON
        elif isinstance(dataset_input, Dict):

            # Assuming entity_pb2_params_from_json is a function that converts JSON to the required parameters
            self._dataset_instance = entity_proto.Entity(
                **dataset_params_from_json(dataset_input))

        # Raise error if neither input is provided
        else:
            raise MantleInvalidParameterError(
                "Either json or proto_entity_object must be provided to create a dataset.")

        self._session = session
        self._storage_client = storage_client
        self._local = local

    def to_proto(self) -> entity_proto.Entity:
        '''
        Convert the dataset to a protocol buffer object.

        Returns:
            entity_proto.Entity: The dataset as a protocol buffer object.

        Example:
            >>> dataset = mantle.dataset.get("dataset_id")
            >>> dataset.to_proto()
        '''
        return self._dataset_instance

    def __str__(self) -> str:
        return self._dataset_instance.__str__()

    def __getattr__(self, name):
        # First, check if the object itself has the property
        # TODO: this should be removed when we deprecate the proto property accessors
        try:
            return super().__getattribute__(name)
        except AttributeError:
            pass

        # If not, then route attribute access to the protobuf object
        if hasattr(self._dataset_instance, name):
            attr = getattr(self._dataset_instance, name)
            if inspect.ismethod(attr):
                return self._wrap_method(attr)
            return attr

        # Handle the case where neither self nor _dataset_instance have the attribute
        raise MantleAttributeError(
            f"'{type(self._dataset_instance).__name__}' object has no attribute '{name}'")

    def _wrap_method(self, method):
        def wrapper(*args, **kwargs):
            return method(*args, **kwargs)
        return wrapper

    def get_property(self, key: str) -> Optional[Message]:
        '''
        Get a property of the dataset.

        Args:
            key (str): The key of the property to get.

        Returns:
            Optional[Message]: The property of the dataset.

        Example:
            >>> dataset = mantle.dataset.get("dataset_id")
            >>> dataset.get_property("property_key")
        '''
        return self._dataset_instance.props.get(key)

    def download_s3(self, key: str, local_path: str):
        '''
        Download a property from S3 to a local path.

        Args:
            key (str): The key of the property to download.
            local_path (str): The local path to download the property to.

        Raises:
            MantleInvalidParameterError: If the property is not an S3 File or is missing required fields.

        Example:
            >>> dataset = mantle.dataset.get("dataset_id")
            >>> dataset.download_s3("property_key", "local/path/to/download")
        '''
        datset_data_value = self._dataset_instance.props.get(key)

        if not datset_data_value or datset_data_value.WhichOneof('value') != 's3_file':
            raise MantleInvalidParameterError(
                f"Property {key} is not an S3 File.")

        s3_file_pb2: data_type_pb2.S3File = datset_data_value.s3_file
        if not s3_file_pb2.IsInitialized():
            raise MantleInvalidParameterError(
                f"S3 File property is missing one or more required fields.")

        self._storage_client.download(
            s3_file_pb2.bucket, s3_file_pb2.key, local_path)

        return

    def upload_s3(self, key: str, local_path: str) -> None:
        '''
        Upload a local file to an S3 property.

        Args:
            key (str): The key of the property to upload.
            local_path (str): The local path of the file to upload.

        Raises:
            MantleInvalidParameterError: If the local file does not exist.

        Example:
            >>> dataset = mantle.dataset.get("dataset_id")
            >>> dataset.upload_s3("property_key", "local/path/to/upload")
        '''
        if not os.path.lexists(local_path):
            raise MantleInvalidParameterError(
                f"Local file {local_path} does not exist.")

        new_file_upload = data_type_pb2.FileUpload(filename=local_path)
        self.set_property(key, new_file_upload)

    def add_s3_file_property(self, key: str, bucket: str, s3_key: str):
        '''
        Add an S3 property to the dataset.

        Args:
            key (str): The key of the property to add.
            bucket (str): The S3 bucket of the property.
            s3_key (str): The S3 key of the property.

        Example:
            >>> dataset = mantle.dataset.get("dataset_id")
            >>> dataset.add_s3_file_property("property_key", "bucket_name", "s3_key")
        '''
        new_s3_file = data_type_pb2.S3File(bucket=bucket, key=s3_key)
        new_dataset_props = DatasetPropertiesBuilder(
        ).build_dataset_props({key: new_s3_file})
        dataset_to_merge = entity_proto.Entity(
            props=new_dataset_props)
        self._dataset_instance.MergeFrom(dataset_to_merge)

    @deprecated("2.0.0", "use name property instead")
    def set_name(self, name: str):
        self._dataset_instance.name = name

    @deprecated("2.0.0", "use data_type property instead")
    def set_data_type(self, data_type: str):
        new_dataset_data_type = data_type_pb2.DataType(unique_id=data_type)
        self.data_type.CopyFrom(new_dataset_data_type)

    def set_property(self, key: str, value: Any):
        '''
        Set a property of the dataset. 

        Args:
            key (str): The key of the property to set.
            value (Any): The value of the property to set.

        Raises:
            MantleInvalidParameterError: If the property value is invalid.
            MantleMissingParameterError: If the property is missing an S3 file or key.


        Example:
            >>> dataset = mantle.dataset.get("dataset_id")
            >>> dataset.set_property("property_key", "property_value")
            >>> dataset.set_property("property_key", 123)
            >>> dataset.set_property("property_key", "s3://bucket/key")
        '''
        new_dataset_data_value = entity_proto.EntityDataValue(
            **validate_dataset_data_value(value))
        self._dataset_instance.props[key].CopyFrom(new_dataset_data_value)
        if not self._local:
            update_props = DatasetPropertiesBuilder().convert_create_dataset_props(
                self._dataset_instance.props)
            update_dataset_request = entity_proto.UpdateEntityRequest(
                name=self._dataset_instance.name, props=update_props)
            res = self._session.make_request(
                "PUT", f"/entity/{self._dataset_instance.unique_id}", data=update_dataset_request)
            if not res.ok:
                res.raise_for_status()

            try:
                dataset_res = entity_proto.EntityResponse()
                dataset_res.ParseFromString(res.content)
                dataset_res_props = dataset_res.entity.props
                for key, val in self._dataset_instance.props.items():
                    if val.WhichOneof('value') == 'file_upload':
                        s3_file_upload_proto = dataset_res_props[key].s3_file
                        if s3_file_upload_proto is None:
                            raise MantleMissingParameterError(
                                f"Property {key} is missing an S3 file.")
                        upload_prefix = s3_file_upload_proto.key
                        if not upload_prefix:
                            raise MantleMissingParameterError(
                                f"Property {key} is missing an S3 file key.")
                        if not upload_prefix:
                            raise MantleMissingParameterError(
                                f"Property {key} is missing an S3 file key.")
                        file_path = val.file_upload.filename
                        self._storage_client.upload(file_path, upload_prefix)
                self._dataset_instance = dataset_res.entity

            except DecodeError as e:
                raise MantleProtoError(
                    res.content, entity_proto.EntityResponse) from e

    @deprecated("2.0.0", "use create() instead")
    def push(self):
        create_props = DatasetPropertiesBuilder().convert_create_dataset_props(
            self._dataset_instance.props)
        create_dataset_request = entity_proto.CreatEntityRequest(
            origin=self._dataset_instance.origin if self._dataset_instance.origin.SerializeToString() else None,
            name=self._dataset_instance.name,
            data_type_id=self._dataset_instance.data_type.unique_id,
            props=create_props
        )
        res = self._session.make_request(
            "POST", f"/entity", data=create_dataset_request)
        if not res.ok:
            res.raise_for_status()
        try:
            dataset_res = entity_proto.EntityResponse()
            dataset_res.ParseFromString(res.content)
            self._dataset_instance = dataset_res.entity
        except DecodeError as e:
            raise MantleProtoError(
                res.content, entity_proto.EntityResponse) from e

    def __setattr__(self, name, value):
        # Check if setting a protobuf field
        if '_dataset_instance' in self.__dict__ and hasattr(self._dataset_instance, name):
            # Update the dataset instance
            setattr(self._dataset_instance, name, value)
            if (self._local):
                return
            update_props = DatasetPropertiesBuilder().convert_create_dataset_props(
                self._dataset_instance.props)
            update_dataset_request = entity_proto.UpdateEntityRequest(
                name=self._dataset_instance.name, props=update_props)
            res = self._session.make_request(
                "PUT", f"/entity/{self._dataset_instance.unique_id}", data=update_dataset_request)
            if not res.ok:
                res.raise_for_status()

            try:
                dataset_res = entity_proto.EntityResponse()
                dataset_res.ParseFromString(res.content)
                dataset_res_props = dataset_res.entity.props
                for key, val in self._dataset_instance.props.items():
                    if val.WhichOneof('value') == 'file_upload':
                        s3_file_upload_proto = dataset_res_props[key].s3_file
                        if s3_file_upload_proto is None:
                            raise MantleMissingParameterError(
                                f"Property {key} is missing an S3 file.")
                        upload_prefix = s3_file_upload_proto.key
                        if not upload_prefix:
                            raise MantleMissingParameterError(
                                f"Property {key} is missing an S3 file key.")
                        self._storage_client.upload(
                            val.file_upload.filename, upload_prefix)
                self._dataset_instance = dataset_res.entity

            except DecodeError as e:
                raise MantleProtoError(
                    res.content, entity_proto.EntityResponse) from e
        else:
            # Regular attribute setting
            super().__setattr__(name, value)

    @property
    @deprecated("2.0.0", "use to_proto() instead")
    def entity_pb2(self) -> entity_proto.Entity:
        return self.to_proto()

    def get_id(self) -> str:
        '''
        Get the ID of the dataset.

        Returns:
            str: The ID of the dataset.

        Example:
            >>> dataset = mantle.dataset.get("dataset_id")
            >>> dataset.get_id()
        '''
        return self._dataset_instance.unique_id

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the dataset to a dictionary.

        Returns:
            Dict[str, Any]: The dataset as a dictionary.

        Example:
            >>> dataset = mantle.dataset.get("dataset_id")
            >>> dataset.to_dict()
        """

        if self._dataset_instance is None:
            return {}

        dataset_dict = {}

        for key, val in self._dataset_instance.props.items():
            dataset_dict.update(data_value_to_dict(key, val))

        dataset_dict['unique_id'] = self._dataset_instance.unique_id
        dataset_dict['created_by_user'] = self._dataset_instance.created_by.name
        dataset_dict['updated_by_user'] = self._dataset_instance.updated_by.name
        dataset_dict['created_at'] = self._dataset_instance.created_at.ToDatetime()
        dataset_dict['updated_at'] = self._dataset_instance.updated_at.ToDatetime()

        return dataset_dict

    def to_series(self) -> pd.Series:
        """
        Convert the dataset to a pandas Series.

        Returns:
            pd.Series: The dataset as a pandas Series.

        Example:
            >>> dataset = mantle.dataset.get("dataset_id")
            >>> dataset.to_series()
        """

        if self._dataset_instance is None:
            return pd.Series()

        return pd.Series(self.to_dict())

    @property
    def entity(self) -> entity_proto.Entity:
        return self._dataset_instance


class MantleEntity(MantleDataset):
    @deprecated("2.0.0", "use MantleDataset instead")
    def __init__(self, entity_input: Union[entity_proto.Entity, Dict[str, Any]], session: _ISession, storage_client: _IStorageClient):
        """ Initialize a dataset. """
        super().__init__(entity_input, session, storage_client)
