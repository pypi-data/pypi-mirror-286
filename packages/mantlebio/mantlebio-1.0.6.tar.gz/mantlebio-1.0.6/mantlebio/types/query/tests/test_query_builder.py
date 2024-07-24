import unittest
from unittest.mock import MagicMock
from mantlebio.exceptions import MantlebioError
from mantlebio.types.query.query_builder import QueryBuilder

class TestQueryBuilder(unittest.TestCase):
    def setUp(self):
        self.client = MagicMock()
        self.query_builder = QueryBuilder(self.client)

    def test_init(self):
        self.assertEqual(self.query_builder.client, self.client)
        self.assertEqual(self.query_builder.query_params, {})
        self.assertFalse(self.query_builder.where_clause)

    def test_validate_condition_invalid_condition(self):
        with self.assertRaises(MantlebioError):
            self.query_builder._validate_condition("invalid_condition")
        
    def test_validate_condition_valid_condition(self):
        self.query_builder._validate_condition("field=value")

    def test_validate_field_with_existing_field(self):
        self.query_builder.query_params["field"] = "value"
        with self.assertRaises(MantlebioError):
            self.query_builder._validate_field("field")
    
    def test_validate_field_with_new_field(self):
        err = None
        try:
            self.query_builder._validate_field("field")
        except MantlebioError as e:
            err = e

        self.assertIsNone(err)

    def test_add_query_condition(self):
        self.query_builder._add_query_condition("field=value")
        self.assertEqual(self.query_builder.query_params, {"field": "value"})



    def test_where_with_existing_query(self):
        self.query_builder.where("field1=value1")
        with self.assertRaises(MantlebioError):
            self.query_builder.where("field2=value2")

    def test_and_with_invalid_condition(self):
        self.query_builder.where("field1=value1")
        with self.assertRaises(MantlebioError):
            self.query_builder.and_("invalid_condition")

    def test_and_with_no_where_clause(self):
        with self.assertRaises(MantlebioError):
            self.query_builder.and_("field=value")
    
    def test_where_and_(self):
        self.query_builder.where("field1=value1")
        self.query_builder.and_("field2=value2")
        self.assertEqual(self.query_builder.query_params, {"field1": "value1", "field2": "value2"})
        self.assertTrue(self.query_builder.where_clause)

    def test_or_(self):
        with self.assertRaises(NotImplementedError):
            self.query_builder.or_("field=value")

    def test_execute_with_no_query_params(self):
        response = self.query_builder.execute()
        self.client.list.assert_called_once_with({})
        self.assertEqual(response, self.client.list.return_value)

    def test_execute_with_query_params(self):
        self.query_builder.where("field1=value1")
        response = self.query_builder.execute()
        self.client.list.assert_called_once_with({"field1": "value1"})
        self.assertEqual(response, self.client.list.return_value)

if __name__ == "__main__":
    unittest.main()