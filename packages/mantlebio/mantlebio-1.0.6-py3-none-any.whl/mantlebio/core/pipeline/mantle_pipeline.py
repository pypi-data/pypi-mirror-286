from abc import abstractmethod
import inspect
from mantlebio.helpers.decorators import deprecated
from proto import pipeline_pb2

from mantlebio.exceptions import MantleAttributeError

class _IPipeline:
    @abstractmethod
    def __init__(self,pipeline_instance: pipeline_pb2.Pipeline)->None:
        pass

    @abstractmethod
    def __getattr__(self, name):
        pass

    @deprecated("2.0.0", "use base object instead")
    @property
    @abstractmethod
    def pipeline_pb2(self)->pipeline_pb2.Pipeline:
        pass
    

class MantlePipeline(_IPipeline):
        
    def __init__(self, pipeline_instance: pipeline_pb2.Pipeline) -> None:
        self._pipeline_instance = pipeline_instance

    def _wrap_method(self, method):
        def wrapper(*args, **kwargs):
            return method(*args, **kwargs)
        return wrapper
    
    @property
    def pipeline_pb2(self)->pipeline_pb2.Pipeline:
        return self._pipeline_instance
    
    def __getattr__(self, name):
        # First, check if the object itself has the property
        # TODO: this should be removed when we deprecate the proto property accessors
        try:
            return super().__getattribute__(name)
        except AttributeError:
            pass

        # Dynamically route attribute access to the protobuf object
        if hasattr(self._pipeline_instance, name):
            attr = getattr(self._pipeline_instance, name)
            if inspect.ismethod(attr):
                return self._wrap_method(attr)
            return attr
        raise MantleAttributeError(f"'{type(self._pipeline_instance).__name__}' object has no attribute '{name}'")
