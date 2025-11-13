#!/usr/bin/env python3
"""
This module contains unit tests for the client module.
"""

import unittest
from parameterized import parameterized
from unittest.mock import patch
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """
    Test class for GithubOrgClient class.

    Contains test cases to verify correct behavior of the
    GithubOrgClient methods.
    """

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name: str,
                 mock_get_json: unittest.mock.Mock) -> None:
        """
        Test that GithubOrgClient.org returns the correct value.

        Args:
            org_name (str): The organization name to test
            mock_get_json (Mock): The mocked get_json function
        """
        # Set up the mock return value
        test_payload = {"login": org_name, "id": 123456}
        mock_get_json.return_value = test_payload

        # Create GithubOrgClient instance
        client = GithubOrgClient(org_name)

        # Call the org property (memoized - accessed as attribute, not method)
        result = client.org

        # Assert that get_json was called once with correct URL
        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)

        # Assert that the result matches the test payload
        self.assertEqual(result, test_payload)


if __name__ == '__main__':
    unittest.main()
