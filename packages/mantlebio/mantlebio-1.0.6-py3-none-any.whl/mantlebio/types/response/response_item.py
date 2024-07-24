from abc import abstractmethod
from google.protobuf import message as _message
import pandas as pd

class ResponseItem():
    @abstractmethod
    def __init__(self, *args, **kwargs) -> None: 
        """ Initialize the response item """
        raise NotImplementedError

    @abstractmethod
    def to_proto(self) -> _message.Message:
        """ Convert the response item to its proto representation """
        raise NotImplementedError
    
    @abstractmethod
    def to_series(self) -> pd.Series:
        """ Convert the response item to a pandas Series """
        pass

