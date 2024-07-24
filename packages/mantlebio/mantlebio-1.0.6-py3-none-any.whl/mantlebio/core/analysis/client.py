from typing import Any, Dict, Optional
from mantlebio.core.analysis.helpers import unmarshall_analysis_proto, validate_analysis_value
from mantlebio.core.analysis.mantle_analysis import MantleAnalysis
from mantlebio.core.dataset.client import _IDatasetClient
from mantlebio.core.session.mantle_session import _ISession
from mantlebio.core.storage.client import _IStorageClient
from mantlebio.helpers.decorators import deprecated
from proto import analysis_pb2


class AnalysisClient:
    """AnalysisClient object for making requests to the Mantle API"""

    def __init__(self, session: _ISession, storage_client: _IStorageClient, dataset_client: _IDatasetClient) -> None:
        """
        Initializes a new instance of the AnalysisClient class.

        Args:
            session (_ISession): The session object used for authentication.
            storage_client (_IStorageClient): The storage client object used for interacting with storage.
            dataset_client (_IDatasetClient): The dataset client object used for interacting with datasets.
        """
        self._session = session
        self._route_stem = f"/analysis/"
        self._storage_client = storage_client
        self._dataset_client = dataset_client
        pass

    def create(self, name: str, inputs: Optional[Dict[str, Any]] = None):
        """Create a new analysis

        Args:
            id (str): Analysis ID
            name (str): Analysis Name
            inputs (optional, dict): Inputs for the analysis

        Returns:
            Analysis: Analysis object

        Examples:
            >>> import mantlebio
            >>> mantle = mantlebio.MantleCient()
            >>> dataset = mantle.dataset.get("dataset_id")
            >>> mantle.analysis.create("My Analysis", {
              "input1": "value1",
              "input2": dataset,
              "input3": "s3://bucket/key",
              "input4": 123
            })
        """
        if inputs:
            new_input_dict = {}
            # a little tricky because we dont want users interacting with proto objects...
            #  so they will pass in a mantle entity and we must extract the pb2 obj
            for in_key, in_val in inputs.items():
                # should also check for other message types(s3 files), but starting with just entities
                value_args = validate_analysis_value(in_val)
                new_input_dict[in_key] = analysis_pb2.AnalysisValue(
                    **value_args)
                inputs = new_input_dict
        else:
            inputs = {}
        input_value_pb2 = analysis_pb2.AnalysisInput(data=inputs)
        create_analysis_req_pb2 = analysis_pb2.CreateAnalysisRequest(
            name=name, inputs=input_value_pb2)
        analysis_resp = self._session.make_request(
            "POST", self._route_stem, data=create_analysis_req_pb2
        )
        # TODO:handle entity creation and storage upload on the (https://mantlebio.atlassian.net/browse/ME-384)
        analysis_pb2_obj = unmarshall_analysis_proto(analysis_resp.content)
        new_analysis = MantleAnalysis(
            analysis_pb2_obj, self._session,  self._storage_client, self._dataset_client)

        return new_analysis

    def get(self, id: str) -> MantleAnalysis:
        """Load an existing analysis

        Args:
            id (str): Analysis ID

        Returns:
            Analysis: Analysis object

        Examples:
            >>> import mantlebio
            >>> mantle = mantlebio.MantleCient()
            >>> analysis = mantle.analysis.get("analysis_id")
        """
        analysis_resp = self._session.make_request(
            "GET", self._route_stem + id
        )

        analysis_pb2_obj = unmarshall_analysis_proto(
            proto_content=analysis_resp.content)

        new_analysis = MantleAnalysis(
            analysis_pb2_obj, self._session, self._storage_client, self._dataset_client)

        return new_analysis
