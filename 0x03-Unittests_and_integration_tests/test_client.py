#!/usr/bin/env python3
"""
This module contains unit tests for the client module.
"""

import unittest
from parameterized import parameterized, parameterized_class
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient

# Import fixtures
try:
    from fixtures import TEST_PAYLOAD
except ImportError:
    # Fallback if fixtures.py doesn't exist
    TEST_PAYLOAD = []


@parameterized_class([
    {
        'org_payload': TEST_PAYLOAD[0][0] if TEST_PAYLOAD else {},
        'repos_payload': TEST_PAYLOAD[0][1] if TEST_PAYLOAD else [],
        'expected_repos': (TEST_PAYLOAD[0][2]
                           if len(TEST_PAYLOAD) > 0
                           and len(TEST_PAYLOAD[0]) > 2
                           else []),
        'apache2_repos': (TEST_PAYLOAD[0][3]
                          if len(TEST_PAYLOAD) > 0 and len(TEST_PAYLOAD[0]) > 3
                          else []),
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration test class for GithubOrgClient.

    Tests the public_repos method with actual method calls
    while only mocking external HTTP requests.
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        Set up class method for integration tests.

        Mocks requests.get to return fixture payloads based on URL.
        """
        # Define side_effect function to return different payloads based on URL
        def get_side_effect(url):
            """
            Side effect function to return appropriate payload based on URL.
            """
            class MockResponse:
                def __init__(self, json_data):
                    self.json_data = json_data

                def json(self):
                    return self.json_data

            if url == "https://api.github.com/orgs/google":
                return MockResponse(cls.org_payload)
            elif url == cls.org_payload.get("repos_url", ""):
                return MockResponse(cls.repos_payload)
            else:
                return MockResponse({})

        # Start patcher for requests.get
        cls.get_patcher = patch('requests.get', side_effect=get_side_effect)
        cls.mock_get = cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Tear down class method for integration tests.

        Stops the patcher.
        """
        cls.get_patcher.stop()

    def test_public_repos(self) -> None:
        """
        Test public_repos method without license filter.
        """
        client = GithubOrgClient("google")
        repos = client.public_repos()
        self.assertEqual(repos, self.expected_repos)

    def test_public_repos_with_license(self) -> None:
        """
        Test public_repos method with Apache 2.0 license filter.
        """
        client = GithubOrgClient("google")
        repos = client.public_repos(license="apache-2.0")
        self.assertEqual(repos, self.apache2_repos)


if __name__ == '__main__':
    unittest.main()
