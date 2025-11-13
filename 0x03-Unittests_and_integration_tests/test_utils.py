#!/usr/bin/env python3
"""
This module contains unit tests for the utils module.
"""

import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock
from utils import access_nested_map, get_json


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


if __name__ == '__main__':
    unittest.main()
