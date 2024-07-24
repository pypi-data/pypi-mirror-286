from mantlebio.core.analysis.client import AnalysisClient
from mantlebio.core.dataset.client import DatasetClient
from mantlebio.core.pipeline.client import PipelineClient
from mantlebio.core.pipeline_run.client import PipelineRunClient
from mantlebio.core.session.mantle_session import MantleSession
from mantlebio.core.auth.creds import AuthMethod
from mantlebio.core.storage.client import StorageClient
from .helpers.decorators import deprecated
from typing import Optional, Dict


class MantleClient:
    """
      Client to interact with MantleBio.
    """

    def __init__(self, tenant_id: Optional[str] = None, env: str = "PROD", credentials: Optional[AuthMethod] = None):
        """
        Initalize MantleClient class object.
        Args:
            tenant_id (optional, str): Tenant ID
            env (optional, str): Environment
        """

        self.session = MantleSession()
        self.session.authenticate(tenant_id, env, creds=credentials)
        self._storage = StorageClient(self.session)
        self._dataset = DatasetClient(self.session, self._storage)
        self._analysis = AnalysisClient(
            self.session, self._storage,  self._dataset)
        self._pipeline_run = PipelineRunClient(
            self.session, self._storage, self._dataset)
        self._pipeline = PipelineClient(self.session)

        pass

    @property
    @deprecated("2.0.0", "Use dataset instead.")
    def entity(self) -> DatasetClient:
        """
        A property that provides access to the dataset object.

        Returns:
            object: The dataset object associated with the instance, typically providing 
            access to dataset-related functionalities or data.

        Note:
            This property encapsulates the internal _dataset attribute, ensuring controlled
            access and potential for additional logic in future updates.
        """
        return self._dataset

    @property
    def dataset(self) -> DatasetClient:
        """
        A property that provides access to the dataset object.

        Returns:
            object: The dataset object associated with the instance, typically providing 
            access to dataset-related functionalities or data.

        Note:
            This property encapsulates the internal _dataset attribute, ensuring controlled
            access and potential for additional logic in future updates.
        """
        return self._dataset

    @property
    def analysis(self) -> AnalysisClient:
        """
        A property that provides access to the analysis object.

        Returns:
            object: The analysis object used for performing or managing various analysis tasks.

        Note:
            This property encapsulates the internal _analysis attribute, ensuring controlled
            access and potential for additional logic in future updates.
        """
        return self._analysis

    @property
    def pipeline(self) -> PipelineClient:
        """
        A property that provides access to the pipeline object.

        Returns:
            object: The pipeline object associated with the instance, used for managing pipelines.

        Note:
            This property encapsulates the internal _pipeline attribute, ensuring controlled
            access and potential for additional logic in future updates.
        """
        return self._pipeline

    @property
    def pipeline_run(self) -> PipelineRunClient:
        """
        A property that provides access to the pipeline run object.

        Returns:
            object: The pipeline run object associated with the instance, used for 
            managing or monitoring pipeline runs.

        Note:
            This property encapsulates the internal _pipeline_run attribute, ensuring 
            controlled access and potential for additional logic in future updates.
        """
        return self._pipeline_run

    @property
    def storage(self):
        """
        A property that provides access to the storage client.

        Returns:
            object: The storage client object for this instance, generally used for 
            interacting with storage services (like databases or cloud storage).

        Note:
            This property encapsulates the internal _storage attribute, ensuring controlled
            access and potential for additional logic in future updates.
        """
        return self._storage

    @property
    @deprecated("2.0.0", "Use pipeline_run instead.")
    def pipeline_run_client(self):
        """
        A deprecated property that provides access to the pipeline run object.

        Returns:
            object: The pipeline run object associated with the instance. This property 
            is deprecated and should be replaced by the 'pipeline' property.

        Deprecated:
            Since version 2.0.0. The 'pipeline' property should be used instead of 
            'pipeline_run_client' in new code.
        """
        return self._pipeline_run

    @deprecated("2.0.0", "Use dataset.create() instead.")
    def create_empty_entity(self):
        '''Creates an Empty Entity to build later

        '''

        return self._dataset.create_empty_entity()

    @deprecated("2.0.0", "Use dataset.create() instead.")
    def create_entity(self, entity_type: str, properties: Optional[Dict] = None, push_now: Optional[bool] = True):
        ''' Create a new Dataset object

        Args:
            entity_type (str): unique id for dataset type to define the new dataset

            properties (optional, dict): properties to be appended to the new dataset

            push_now (optional, bool): if False, a dataset object will be created but 
                only saved locally. If True, the object will be posted to the mantle 
                API within the context of the current session

        Returns:
            Dataset: Dataset object
        '''
        if not push_now:
            return self._dataset.create_local_entity(entity_type, properties)
        else:
            return self._dataset.create_cloud_entity(entity_type, properties)

    @deprecated("2.0.0", "Use dataset.get() instead.")
    def get_entity(self, entity_id: str):
        """Get an entity

        Args:
            entity_id (str): Entity ID

        Returns:
            Entity: Entity object
        """
        return self._dataset.get_entity(entity_id)

    @deprecated("2.0.0", "Use dataset.get_all() instead.")
    def get_entities(self):
        """Get all Datasets

        Returns:
            list: List of Dataset objects
        """
        return self._dataset.get_entities()

    @deprecated("2.0.0", "Use analysis.load() instead.")
    def load_analysis(self, id: str):
        """Load an existing analysis

        Args:
            id (str): Analysis ID

        Returns:
            Analysis: Analysis object
        """
        return self._analysis.load_analysis(id)

    @deprecated("2.0.0", "Use analysis.create() instead.")
    def new_analysis(self, name: str):
        """Create a new analysis

        Args:
            analysis_id (str): Analysis ID
            name (str): Analysis Name

        Returns:
            Analysis: Analysis object
        """
        return self._analysis.create(name)

    @deprecated("2.0.0", "Use pipeline_run.kickoff() instead.")
    def kick_off_pipeline_run(self, pipeline_id: str, pipeline_version: str, input_vals: Optional[dict] = None, exteral=False):
        """Create a new pipeline

        Args:
            pipeline_id (str): Pipeline ID
            name (str): Pipeline Name

        Returns:
            Analysis: Pipeline Run Object
        """
        return self._pipeline_run.kickoff_run(pipeline_id, pipeline_version, input_vals, external=exteral)

    @deprecated("2.0.0", "Use pipeline_run.get() instead.")
    def load_pipeline(self, pipeline_run_id: str):
        """Load an existing pipeline

        Args:
            pipeline_run_id (str): Pipeline Run ID

        Returns:
            Analysis: Analysis object
        """
        return self._pipeline_run.load_run(pipeline_run_id)

    @deprecated("2.0.0", "Use pipeline.get() instead.")
    def get_pipeline(self, pipeline_id):
        """ Send Get Pipeline request to api

        Args:
            pipeline_id (str): the unique id of the pipeline

        Returns:
            Pipeline: Pipeline    
        """
        return self._pipeline.get_pipeline(pipeline_id)

    def close(self):
        """Close the MantleClient"""
        self.session.sign_out()
