

from mantlebio.core.pipeline.mantle_pipeline import _IPipeline, MantlePipeline
from mantlebio.core.session.mantle_session import _ISession
from mantlebio.exceptions import MantleMissingParameterError
from mantlebio.helpers.decorators import deprecated
from proto import pipeline_pb2
from google.protobuf.message import DecodeError


class PipelineClient:
    """PipelineClient object for making requests to the Mantle API"""

    def __init__(self, session: _ISession) -> None:

        self.session = session
        self.route_stem = f"/pipeline/"
        pass

    @deprecated("2.0.0", "use get() instead")
    def get_pipeline(self, id: str, version: str = "") -> _IPipeline:
        """get an existing Pipeline

        Args:
            id (str): Pipeline ID

        Returns:
            Pipeline: Pipeline object

        Note:
            This method will be deprecated in version 2.0.0. Use get() instead.
        """
        return self.get(id, version)

    def get(self, id: str, version: str = "") -> _IPipeline:
        """get an existing Pipeline

        Args:
            id (str): Pipeline ID
            version (str, optional): Pipeline Version. Defaults to "". If not provided, the latest version will be returned.

        Returns:
            Pipeline: Pipeline object

        Examples:
            >>> mantle = mantlebio.MantleClient()
            >>> pipeline = mantle.pipeline.get("pipeline_id")
        """

        if not id:
            raise MantleMissingParameterError("id is required")

        endpoint = f"{self.route_stem}{id}/{version}"
        if not version:
            # By default, the latest version will be returned so we dont want to raise an error but we want to log a warning since it could lead to unexpected behavior
            Warning("No version provided. The latest version will be returned.")
            endpoint = f"{self.route_stem}{id}"

        res = self.session.make_request("GET", endpoint)

        if not res.ok:
            res.raise_for_status()

        try:
            pipeline_proto = pipeline_pb2.Pipeline()
            pipeline_proto.ParseFromString(res.content)

        except DecodeError as e:
            raise

        return MantlePipeline(pipeline_proto)
