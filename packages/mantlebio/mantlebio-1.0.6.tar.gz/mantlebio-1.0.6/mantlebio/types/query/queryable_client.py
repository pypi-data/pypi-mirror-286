
from abc import abstractmethod

from mantlebio.types.response.list_reponse import ListResponse
from mantlebio.types.response.response_item import ResponseItem


class QueryableClient():
    def __init__(self, *args, **kwargs):
        pass
    
    @abstractmethod
    def build_query(self):
        raise NotImplementedError
    
    @abstractmethod
    def list(self)->ListResponse[ResponseItem]:
        raise NotImplementedError