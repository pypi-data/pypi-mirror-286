from typing import Generic, TypeVar

from mantlebio.exceptions import MantleQueryBuilderError, MantlebioError
from mantlebio.types.query.queryable_client import QueryableClient
from mantlebio.types.response.list_reponse import ListResponse
from mantlebio.types.response.response_item import ResponseItem

T = TypeVar('T', bound=QueryableClient)

class QueryBuilder(Generic[T]):
    """
    A generic query builder class for constructing queries to be executed by a QueryableClient.

    Args:
        client (T): The QueryableClient instance to execute the query.

    Attributes:
        client (T): The QueryableClient instance to execute the query.
        query_params (dict): The dictionary containing the query parameters.

    """

    def __init__(self, client: T):
        self.client = client
        self.where_clause = False
        self.query_params = {}

    def _validate_condition(self, condition: str):
        """
        Helper method to validate the query condition.

        Args:
            condition (str): The condition to validate.

        Raises:
            MantleQueryBuilderError: If the condition format is invalid.

        """
        if "=" not in condition or len(condition.split("=")) != 2:
            raise MantleQueryBuilderError(f"Invalid query condition '{condition}'")
        
    def _validate_field(self, field: str):
        """
        Helper method to validate the query field.

        Args:
            field (str): The field to validate.

        Raises:
            MantleQueryBuilderError: If the field has already been added to the query.

        """
        if self.query_params.get(field):
            raise MantleQueryBuilderError(f"Field '{field}' already set for the query")

    def _add_query_condition(self, condition: str):
        """
        Helper method to add a query condition to the query.

        Args:
            condition (str): The condition to add.

        Raises:
            MantleQueryBuilderError: If the condition format is invalid.
            MantleQueryBuilderError: If the field has already been added to the query.
        """

        self._validate_condition(condition)
        field, value = condition.split("=")

        # strip any leading/trailing whitespace
        field = field.strip()
        value = value.strip()

        self._validate_field(field)

        self.query_params[field] = value

    def where(self, condition: str):
        """
        Adds a WHERE condition to the query.

        Args:
            condition (str): The condition to add.

        Examples:
            >>> query_builder.where("field1=value1")
            >>> query_builder.where("props{field2}.string.eq=value2")

        Returns:
            QueryBuilder: The QueryBuilder instance.

        Raises:
            MantleQueryBuilderError: If a where condition already exists in query.
            MantleQueryBuilderError: If the condition format is invalid.
            MantleQueryBuilderError: If the field has already been added to the query.
        """
        if self.query_params:
            raise MantleQueryBuilderError("Only one WHERE condition is allowed in a query")
        
        self._add_query_condition(condition)

        self.where_clause = True
        
        return self

    def and_(self, condition: str):
        """
        Adds an AND condition to the query.

        Args:
            condition (str): The condition to add.

        Examples:
            >>> query_builder.where("field1=value1").and_("field2=value2")
            >>> query_builder.where("props{field1}.string.eq=value1").and_("field2=value2")

        Returns:
            QueryBuilder: The QueryBuilder instance.

        Raises:
            MantleQueryBuilderError: If there is no WHERE condition in the query.
            MantleQueryBuilderError: If the condition format is invalid.
            MantleQueryBuilderError: If the field has already been added to the query.
        """
        if not self.where_clause:
            raise MantleQueryBuilderError("Cannot add AND condition without a WHERE condition")
        
        self._add_query_condition(condition)
        
        return self

    def or_(self, condition: str):
        """
        Adds an OR condition to the query.

        Args:
            condition (str): The condition to add.

        Raises:
            NotImplementedError: This method is not implemented.

        """
        raise NotImplementedError


    def execute(self)-> ListResponse[ResponseItem]:
        """
        Executes the query and returns the response.

        Examples:
            >>> response = query_builder.where("field1=value1").execute()
            >>> response = query_builder.where("field1=value1").and_("field2=value2").execute()

        Returns:
            ListResponse: The response from executing the query.

        """
        response = self.client.list(self.query_params)
        return response