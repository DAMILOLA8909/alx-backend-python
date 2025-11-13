#!/usr/bin/env python3
"""
This module contains unit tests for the client module.
"""

import unittest
from parameterized import parameterized
from unittest.mock import patch, PropertyMock
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

    def test_public_repos_url(self) -> None:
        """
        Test that _public_repos_url returns the expected value.

        Mocks the org property to return a known payload and verifies
        that _public_repos_url extracts the correct repos_url.
        """
        # Known payload to use for mocking
        test_payload = {
            "login": "test_org",
            "id": 123456,
            "repos_url": "https://api.github.com/orgs/test_org/repos"
        }

        # Patch the org property to return our test payload
        with patch('client.GithubOrgClient.org',
                   new_callable=PropertyMock,
                   return_value=test_payload):
            # Create GithubOrgClient instance
            client = GithubOrgClient("test_org")

            # Call the _public_repos_url property
            result = client._public_repos_url

            # Assert that the result matches the expected repos_url
            expected_url = "https://api.github.com/orgs/test_org/repos"
            self.assertEqual(result, expected_url)


if __name__ == '__main__':
    unittest.main()
