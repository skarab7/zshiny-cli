import unittest
from shiny_client import client


class ZClientTest(unittest.TestCase):

    def test_discover_resources(self):
        """
        """
        c = client.Client()
        c.discover_resources("https://api.zalando.com")
        print("xx")
