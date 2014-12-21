import unittest
from shiny_client import client
from shiny_client import category
import jsonschema
import json


class TestResources(unittest.TestCase):

    def test_category_manager(self):
        mgmt = category.CategoryManager()
        mgmt.resource_url = "http://api.zalando.com:80/categories"
        mgmt.api_lang = "pl-PL"
        for c in mgmt.list():
            print("===")
            print(c.name)
            print(c.key)
            print(c.targetGroup)
            print(c.childKeys)
            print(c.parentKey)

    def test_integration_with_api(self):
        mgmt = category.CategoryManager()
        js = mgmt.get_schema()
        print(js)
        json_schema = json.loads(js)
        j = json.loads("""
        {
    "key": "women",
    "name": "Women",
    "parentKey": "catalog",
    "childKeys": ["womens-shoes", "womens-clothing", "sports-womens", "premium-womens"],
    "type": "default",
    "outlet": false,
    "hidden": false,
    "targetGroup": "WOMEN"
    }""")
        jsonschema.validate(j, json_schema)
