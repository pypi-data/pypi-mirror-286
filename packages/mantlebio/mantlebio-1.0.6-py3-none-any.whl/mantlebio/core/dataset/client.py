
from abc import abstractmethod
from typing import Any, Dict, Iterable, Optional
import warnings
from mantlebio.core.dataset.helpers import DatasetPropertiesBuilder, unmarshall_dataset
from mantlebio.core.dataset.mantle_dataset import _IDataset, MantleDataset
from mantlebio.core.session.mantle_session import _ISession
from mantlebio.core.storage.client import _IStorageClient
from mantlebio.exceptions import MantleInvalidParameterError, MantleMissingParameterError, MantleProtoError
from mantlebio.helpers.decorators import deprecated
from mantlebio.types.query.query_builder import QueryBuilder
from mantlebio.types.query.queryable_client import QueryableClient
from mantlebio.types.response.list_reponse import ListResponse
from proto import entity_pb2
from google.protobuf.message import DecodeError


class _IDatasetClient(QueryableClient):
    """
    Interface for an entity client that interacts with entities in a data storage system.
    """

    @abstractmethod
    def __init__(self, session: _ISession, storage_client: _IStorageClient, analysis_id: str = "", pipeline_run_id: str = "") -> None:
        pass

    @abstractmethod
    def get(self, id: str) -> _IDataset:
        """
        Retrieves an entity by its ID.

        Args:
            id (str): The ID of the entity.

        Returns:
            _IEntity: The retrieved entity.
        """
        raise NotImplementedError

    @abstractmethod
    def get_entities(self) -> ListResponse[_IDataset]:
        """
        Retrieves all entities.

        Returns:
            ListResponse[_IEntity]: An Iterable List of all entities.
        """
        raise NotImplementedError

    @abstractmethod
    def get_datasets(self) -> ListResponse[_IDataset]:
        """
        Retrieves all datasets.

        Returns:
            ListResponse[_IDataset]: An Iterable List of all datasets.
        """
        raise NotImplementedError

    @abstractmethod
    def list(self, query_params: Dict[str, str] = {}) -> ListResponse[_IDataset]:
        """
        Retrieves a list of entities.

        Returns:
            ListResponse[_IEntity]: An Iterable List of entities.
        """
        raise NotImplementedError

    @abstractmethod
    def create(self, name: Optional[str] = None, dataset_type: Optional[str] = None, properties: Optional[Dict[str, Any]] = None, local: bool = True, origin: Optional[entity_pb2.Origin] = None, entity_type: Optional[str] = None) -> _IDataset:
        """
        Creates a new dataset.

        Args:
            dataset_type (str, optional): The type of the dataset. Defaults to None.
            properties (Dict[str,Any], optional): The properties of the dataset. Defaults to None.
            local (bool, optional): Whether the dataset is local. Defaults to True.
            origin (entity_pb2.Origin, optional): The origin of the dataset. Defaults to None.
            entity_type (str, optional): The type of the entity. Defaults to None. This is a deprecated parameter. Will be removed in 2.0.0.

        Returns:
            _IDataset: The created dataset.
        """
        raise NotImplementedError


class DatasetClient(_IDatasetClient):
    """DatasetClient object for making requests to the Mantle API"""

    def __init__(self, session: _ISession, storage_client: _IStorageClient, analysis_id: str = "", pipeline_run_id: str = "") -> None:
        self._session = session
        self._storage_client = storage_client
        self._route_stem = f"/entity"
        self._analysis_id = analysis_id
        self._pipeline_run_id = pipeline_run_id

    def get(self, id: str) -> _IDataset:
        """Get a dataset by ID

        Args:
            id (str): Dataset ID

        Returns:
            Dataset: Dataset object

        Examples:
            >>> import mantlebio
            >>> mantle = mantlebio.MantleClient()
            >>> dataset = mantle.dataset.get("dataset_id")
        """
        res = self._session.make_request("GET", f"{self._route_stem}/{id}")

        if not res.ok:
            res.raise_for_status()

        try:
            dataset = entity_pb2.EntityResponse()
            dataset.ParseFromString(res.content)

        except DecodeError as e:
            raise MantleProtoError(
                res.content, entity_pb2.EntityResponse) from e

        return MantleDataset(dataset_input=dataset.entity, session=self._session, storage_client=self._storage_client)

    @deprecated("2.0.0", "use get() instead")
    def get_entity(self, id: str) -> _IDataset:
        """Get a dataset by ID

        Args:
            id (str): Dataset ID

        Returns:
            Dataset: Dataset object

        Examples:

            >>> import mantlebio
            >>> mantle = mantlebio.MantleClient()
            >>> dataset = mantle.dataset.get_entity("dataset_id")
        """
        return self.get(id)

    @deprecated("2.0.0", "use list() instead")
    def get_entities(self) -> Iterable[_IDataset]:
        """Get a list of Datasets

        Returns:
            list: List of Dataset objects

        Examples:
              >>> import mantlebio
              >>> mantle = mantlebio.MantleClient()
              >>> datasets = mantle.dataset.get_entities()
        """
        return self.get_datasets()

    @deprecated("2.0.0", "use list() instead")
    def get_datasets(self) -> Iterable[_IDataset]:
        """Gets a list of all Datasets

        Returns:
            list: List of Dataset objects

        Examples:
              >>> import mantlebio
              >>> mantle = mantlebio.MantleClient()
              >>> datasets = mantle.dataset.get_datasets()
              >>> for dataset in datasets:
              >>>     print(dataset.get_id())
        """
        return self.list()

    def build_query(self) -> QueryBuilder:
        '''Build a query for datasets

        Returns:
            QueryBuilder: QueryBuilder object

        Examples:
            >>> import mantlebio
            >>> mantle = mantlebio.MantleClient()
            >>> # query by data type
            >>> query = mantle.dataset.build_query().where("data_type_unique_id=plate").execute()
            >>> # query by property
            >>> query = mantle.dataset.build_query().where("props.{foo}.string.eq=bar").execute()
        '''
        return QueryBuilder(self)

    def list(self, query_params: Dict[str, str] = {}) -> ListResponse[_IDataset]:
        """Get a list of datasets

        Note: To query datasets, use the build_query method.

        Returns:
            ListResponse[Dataset]: List of Dataset objects

        Examples:
            >>> import mantlebio
            >>> mantle = mantlebio.MantleClient()
            >>> datasets = mantle.dataset.list()
            >>>  for dataset in datasets:
            >>>     print(dataset.get_id())
        """
        # will need refactor for repeated objects

        datasets = ListResponse[_IDataset]()

        try:
            has_next_token = True

            while has_next_token:
                res = self._session.make_request(
                    "GET", self._route_stem, params=query_params)

                if not res.ok:
                    res.raise_for_status()

                dataset_list = entity_pb2.EntitiesResponse()
                dataset_list.ParseFromString(res.content)
                for dataset in dataset_list.entities:
                    datasets.append(MantleDataset(
                        dataset_input=dataset, session=self._session, storage_client=self._storage_client))
                has_next_token = dataset_list.next_page_token != ""
                query_params['page_token'] = dataset_list.next_page_token

        except DecodeError as e:
            raise MantleProtoError(
                res.content, entity_pb2.EntitiesResponse) from e

        return datasets

    def _create_local_dataset(self, name: Optional[str] = None, dataset_type: Optional[str] = None, properties: Optional[Dict[str, Any]] = None, origin: Optional[entity_pb2.Origin] = None) -> _IDataset:
        dataset_params_json = {}
        if not properties:
            properties = {}
        if dataset_type:
            dataset_params_json.update(
                {"data_type": {"unique_id": dataset_type}})
        if name:
            dataset_params_json.update({"name": name})
        dataset_params_json.update({"props": properties})
        if origin:
            dataset_params_json.update({"origin": origin})
        return MantleDataset(dataset_input=dataset_params_json, session=self._session, storage_client=self._storage_client, local=True)

    def _create_cloud_dataset(self, dataset_type: str, properties: Optional[Dict[str, Any]] = None, origin: Optional[entity_pb2.Origin] = None, name: Optional[str] = None) -> _IDataset:
        if not properties:
            properties = {}

        property_builder = DatasetPropertiesBuilder()

        dataset_props = property_builder.build_create_dataset_props(
            properties)

        dataset_req = entity_pb2.CreatEntityRequest(
            name=name,
            data_type_id=dataset_type,
            props=dataset_props,
            origin=origin
        )

        res = self._session.make_request(
            "POST", self._route_stem, data=dataset_req)

        if not res.ok:
            res.raise_for_status()

        dataset_res = unmarshall_dataset(res.content)

        for key, val in dataset_props.items():
            if val.WhichOneof('value') == 'file_upload':
                s3_file_upload_proto = dataset_res.props[key].s3_file
                if s3_file_upload_proto is None:
                    raise MantleMissingParameterError(
                        f"Property {key} is missing an S3 file.")
                upload_prefix = s3_file_upload_proto.key
                if not upload_prefix:
                    raise MantleMissingParameterError(
                        f"Property {key} is missing an S3 file key.")
                self._storage_client.upload(
                    val.file_upload.filename, upload_prefix)

        return MantleDataset(dataset_input=dataset_res, session=self._session, storage_client=self._storage_client)

    def create(self, name: Optional[str] = None, dataset_type: Optional[str] = None, properties: Optional[Dict[str, Any]] = None, local: bool = True, origin: Optional[entity_pb2.Origin] = None, entity_type: Optional[str] = None) -> _IDataset:
        if entity_type:
            warnings.warn(f"entity_type parameter is deprecated and will be removed in version 2.0.0. Use dataset_type instead.",
                          category=DeprecationWarning, stacklevel=2)
            dataset_type = entity_type
        if local:
            return self._create_local_dataset(name, dataset_type, properties, origin)
        else:
            return self._create_cloud_dataset(dataset_type, properties, origin, name=name)

    @deprecated("2.0.0", "use create() instead.")
    def create_cloud_entity(self, entity_type: str, properties: Optional[Dict[str, Any]] = None) -> _IDataset:
        return self.create(dataset_type=entity_type, properties=properties, local=False)

    @deprecated("2.0.0", "use create() instead.")
    def create_local_entity(self, entity_type: Optional[str] = None, properties: Optional[Dict[str, Any]] = None) -> _IDataset:
        return self.create(dataset_type=entity_type, properties=properties, local=True)

    @deprecated("2.0.0", "use create() instead.")
    def create_empty_entity(self):
        return self.create_local_entity()


class EntityClient(DatasetClient):
    @deprecated("2.0.0", "Use DatasetClient instead")
    def __init__(self, session: _ISession, storage_client: _IStorageClient, analysis_id: str = "", pipeline_run_id: str = "") -> None:
        super().__init__(session, storage_client, analysis_id, pipeline_run_id)
