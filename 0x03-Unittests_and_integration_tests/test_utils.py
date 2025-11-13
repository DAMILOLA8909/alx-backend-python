#!/usr/bin/env python3
"""
This module contains unit tests for the utils module.
"""

import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """
    Test class for access_nested_map function.

    Contains test cases to verify correct behavior when accessing
    values in nested dictionaries.
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map: dict, path: tuple,
                               expected: any) -> None:
        """
        Test that access_nested_map returns the expected result.

        Args:
            nested_map (dict): The nested dictionary to access
            path (tuple): The path of keys to traverse
            expected (any): The expected value at the specified path
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), "a"),
        ({"a": 1}, ("a", "b"), "b"),
    ])
    def test_access_nested_map_exception(self, nested_map: dict, path: tuple,
                                         expected_key: str) -> None:
        """
        Test that access_nested_map raises KeyError with expected message.

        Args:
            nested_map (dict): The nested dictionary to access
            path (tuple): The path of keys to traverse
            expected_key (str): The expected key in the exception message
        """
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)

        self.assertEqual(str(context.exception), f"'{expected_key}'")


class TestGetJson(unittest.TestCase):
    """
    Test class for get_json function.

    Contains test cases to verify correct behavior when fetching
    JSON data from remote URLs.
    """

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url: str, test_payload: dict) -> None:
        """
        Test that get_json returns the expected result.

        Args:
            test_url (str): The URL to test
            test_payload (dict): The expected JSON payload
        """
        # Create a mock response object with json method
        mock_response = Mock()
        mock_response.json.return_value = test_payload

        # Patch requests.get to return our mock response
        with patch('utils.requests.get',
                   return_value=mock_response) as mock_get:
            # Call the function
            result = get_json(test_url)

            # Assert that requests.get was called exactly once with test_url
            mock_get.assert_called_once_with(test_url)

            # Assert that the result equals test_payload
            self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """
    Test class for memoize decorator.

    Contains test cases to verify correct behavior of the
    memoization functionality.
    """

    def test_memoize(self) -> None:
        """
        Test that memoize decorator caches method results.

        Verifies that when a memoized property is called twice,
        the underlying method is only executed once.
        """
        class TestClass:
            """
            Test class with a method and memoized property.
            """

            def a_method(self) -> int:
                """
                Method that returns a constant value.

                Returns:
                    int: The value 42
                """
                return 42

            @memoize
            def a_property(self) -> int:
                """
                Memoized property that calls a_method.

                Returns:
                    int: The result from a_method
                """
                return self.a_method()

        # Create instance of TestClass
        test_instance = TestClass()

        # Mock the a_method to track calls and return value
        with patch.object(TestClass, 'a_method',
                          return_value=42) as mock_a_method:
            # Call a_property twice
            result1 = test_instance.a_property
            result2 = test_instance.a_property

            # Assert that both calls return the correct result
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)

            # Assert that a_method was called only once
            mock_a_method.assert_called_once()


if __name__ == '__main__':
    unittest.main()
