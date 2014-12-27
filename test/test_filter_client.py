import unittest
from shiny_client import article_filter
import jsonschema
import json
import requests
import os


class TestFilterClient(unittest.TestCase):

    API_LANG = os.getenv("SHINY_CLIENT_TEST_API_LANG", "pl-PL")
    RESOURCE_URL = "https://api.zalando.com/filters"

    def test_filter_list(self):
        mgnt = self._get_resource_mgmt()

        for c in mgnt.list():
            print(c.name)

    def _get_resource_mgmt(self):
        mgmt = article_filter.FilterManager()
        mgmt.resource_url = TestClient.RESOURCE_URL
        mgmt.api_lang = TestCategoryClient.API_LANG
        return mgmt
