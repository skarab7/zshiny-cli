import unittest
from shiny_client import client
from shiny_client import category
import jsonschema
import json


class TestResources(unittest.TestCase):

    def test_category_manager(self):
        mgmt = self._get_category_mgmt()

        for c in mgmt.list_page(2):
            self.assertIsNotNone(c.name)
            self.assertIsNotNone(c.key)
            self.assertIsNotNone(c.targetGroup)
            self.assertIsNotNone(c.childKeys)
            self.assertTrue(c.parentKey is None or isinstance(c.parentKey, str))

    def _get_category_mgmt(self):
        mgmt = category.CategoryManager()
        mgmt.resource_url = "http://api.zalando.com:80/categories"
        mgmt.api_lang = "pl-PL"
        return mgmt

    def test_integration_with_api(self):
        """
        Check whether the CLI creator understands the API.
        Test against the changes in schema of category
        """
        mgmt = self._get_category_mgmt()
        r = mgmt._do_request({})
        for i in range(10):
            category_json = r.json()["content"][i]
            js = mgmt.get_schema()
            json_schema = json.loads(js)
            jsonschema.validate(category_json, json_schema)

    def test_find_by_name_and_outlet(self):
        mgmt = self._get_category_mgmt()
        query = {"name": "Szaliki kominy", "targetGroup": "WOMEN",
                 "outlet": True}

        for c in mgmt.find_by(query):
            self.assertTrue(c.outlet)
            self.assertContains(c.name.lower(), "szalik")
            self.assertContains(c.name.lower(), "kominy")
