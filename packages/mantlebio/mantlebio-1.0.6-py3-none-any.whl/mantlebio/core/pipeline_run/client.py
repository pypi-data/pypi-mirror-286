from typing import Dict, Optional

from mantlebio.core.dataset.client import _IDatasetClient
from mantlebio.core.pipeline_run.helpers import MantlePipelineRunKickoff
from mantlebio.core.pipeline_run.mantle_pipeline_run import _IPipelineRun, MantlePipelineRun
from mantlebio.core.session.mantle_session import _ISession
from mantlebio.core.storage.client import _IStorageClient
from mantlebio.exceptions import MantleConfigurationError
from mantlebio.helpers.decorators import deprecated
from proto import data_type_pb2, pipeline_run_pb2


class PipelineRunClient:
    """PipelineRunClient object for making pipeline run requests to the Mantle API"""

    def __init__(self, session: _ISession, storage_client: _IStorageClient, dataset_client: _IDatasetClient) -> None:
        self.session = session
        self._route_stem = f"/pipeline_run/"
        self.storage_client = storage_client
        self.dataset_client = dataset_client
        self.entity_client = self.dataset_client
        pass

    @deprecated("2.0.0", "use get() instead")
    def load_run(self, id: str) -> _IPipelineRun:
        """Load an existing Pipeline Run

        Args:
            id (str): Pipeline ID

        Returns:
            PipelineRun: PipelineRun object

        Note: Will be deprecated in version 2.0.0 in favor of pipeline_run.get()
        """
        return self.get(id)

    @deprecated("2.0.0", "use kickoff() instead")
    def kickoff_run(self, pipeline_id: str, version: str, input: Optional[Dict] = None, external: bool = False) -> _IPipelineRun:
        """Create a new Pipeline Run

        Args:
            id (str): Pipeline ID
            version (str): Pipeline Version
            input (dict, optional): Pipeline Run inputs

        Returns:
            PipelineRun: PipelineRun object

        Note: Will be deprecated in version 2.0.0 in favor of kickoff()
        """
        return self.kickoff(pipeline_id, version, input, external)

    def kickoff(self, pipeline_id: str, version: str, input: Optional[Dict] = None, external: bool = False) -> _IPipelineRun:
        '''
        Kickoff a new pipeline run.

        Args:
            pipeline_id (str): The pipeline ID
            version (str): The pipeline version
            input (dict, optional): The pipeline run inputs
            external (bool, optional): If the pipeline run is external that means it is not managed by Mantle.

        Returns:
            PipelineRun: The pipeline run object

        Examples:
            >>> import mantlebio
            >>> mantle = mantlebio.MantleClient()
            >>> pipeline_run = mantle.pipeline_run.kickoff("pipeline_id", "version", {
                "input1": "value1",
                "input2": "value2",
                "input3": "s3://bucket/key",
                "input4": 123
            })
        '''
        if not pipeline_id and version:
            raise MantleConfigurationError(
                "Cannot create new pipleine run without pipeline ID and version.")

        pipeline_kickoff = MantlePipelineRunKickoff(
            pipeline_id=pipeline_id,
            pipeline_version=version,
            external=external,
            inputs=input
        )

        pipeline_run = MantlePipelineRun(
            pipeline_kickoff, self.session, self.storage_client, self.dataset_client)

        if not input:
            return pipeline_run
        # after kicking off the pipeline, upload the inputs to storage.
        for field in input.keys():
            if not isinstance(input[field], data_type_pb2.FileUpload):
                continue
            # upload file to storage
            self.storage_client.upload(
                path=input[field].path,
                upload_key=f"runs/{pipeline_run.unique_id}/input/{field}/{input[field].name}"
            )

        return pipeline_run

    @deprecated("2.0.0", "use get().updated_statue() instead")
    def update_status(self, id: str, status: str):
        pipeline_run = self.get(id)

        pipeline_run.update_status(status)

    def get(self, id: str) -> _IPipelineRun:
        '''
        Get a pipeline run by ID.

        Args:
            id (str): The pipeline run ID

        Returns:
            PipelineRun: The pipeline run object

        Examples:
            >>> import mantlebio
            >>> mantle = mantlebio.MantleClient()
            >>> pipeline_run = mantle.pipeline_run.get("pipeline_run_id")
        '''
        res = self.session.make_request(
            "GET", f"{self._route_stem}{id}")

        if not res.ok:
            res.raise_for_status()

        pipeline_run_obj_pb2 = pipeline_run_pb2.PipelineRun()
        pipeline_run_obj_pb2.ParseFromString(res.content)
        return MantlePipelineRun(pipeline_run_obj_pb2, self.session, self.storage_client, self.dataset_client)
