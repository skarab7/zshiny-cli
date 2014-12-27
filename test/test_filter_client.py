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
            self.assertIsNotNone(c.name)

    def _get_resource_mgmt(self):
        mgmt = article_filter.FilterManager()
        mgmt.resource_url = TestFilterClient.RESOURCE_URL
        mgmt.api_lang = TestFilterClient.API_LANG
        return mgmt

    def test_integration_with_api(self):
        mgmt = self._get_resource_mgmt()
        r = mgmt._do_request({})
        for i in range(10):
            object_as_json = r.json()[i]
            js = mgmt.get_schema()
            json_schema = json.loads(js)
            jsonschema.validate(object_as_json, json_schema)
