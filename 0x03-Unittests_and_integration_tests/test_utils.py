#!/usr/bin/env python3
"""
This module contains unit tests for the utils module.
"""

import unittest
from parameterized import parameterized
from utils import access_nested_map


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


if __name__ == '__main__':
    unittest.main()
