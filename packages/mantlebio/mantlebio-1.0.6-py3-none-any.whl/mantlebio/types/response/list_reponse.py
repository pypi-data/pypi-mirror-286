from typing import List, Type, TypeVar, Generic, Iterator, Union
import pandas as pd

from mantlebio.exceptions import MantleResponseError
from mantlebio.types.response.response_item import ResponseItem

T = TypeVar('T', bound=ResponseItem)

class ListResponse(Generic[T]):
    """
    A generic class for handling list responses from the Mantle API
    """
    def __init__(self, items: Union[List[T],None] = None) -> None:
        self.items = items if items else [] 

    def __len__(self) -> int:
        return len(self.items)
    
    def __getitem__(self, index: int) -> T:
        return self.items[index]

    def __iter__(self) -> Iterator[T]:
        return iter(self.items)
    
    def append(self, item: T) -> None:
        """
        Append an item to the list
        """
        self.items.append(item)

    def extend(self, items: List[T]) -> None:
        """
        Extend the list with a list of items
        """
        self.items.extend(items)
    
    def to_dataframe(self) -> pd.DataFrame:
        """
        Convert the list of items to a pandas DataFrame
        """
        try:
            data = [item.to_series() for item in self.items]
            return pd.DataFrame(data)
        except Exception as e:
            raise MantleResponseError("Error converting list response to DataFrame") from e
        
    def _get_item_type(self) -> Type[T]:
        if self.items and len(self.items) > 0:
            return type(self.items[0])
        raise ValueError("The items list is empty, cannot determine the item type.")
