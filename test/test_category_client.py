import unittest
from shiny_client import category
import requests
from base_test import ApiResourceTest


class TestCategoryClient(ApiResourceTest, unittest.TestCase):

    RESOURCE_URL = "https://api.zalando.com/categories"

    def _assert_resouce_list_test(self, o):
        self.assertIsNotNone(o.name)
        self.assertIsNotNone(o.key)
        self.assertIsNotNone(o.targetGroup)
        self.assertIsNotNone(o.childKeys)
        self.assertTrue(o.parentKey is None or isinstance(o.parentKey, str))

    def _create_resource_mgmt(self):
        return category.CategoryManager()

    def _get_resource_endpoint(self):
        return TestCategoryClient.RESOURCE_URL

    def test_find_by_name_and_outlet(self):
        mgmt = self._get_resource_mgmt()
        query = {"name": "Szaliki kominy", "targetGroup": "WOMEN",
                 "outlet": True}

        for c in mgmt.find_by(query):
            self.assertTrue(c.outlet)
            self.assertContains(c.name.lower(), "szalik")
            self.assertContains(c.name.lower(), "kominy")

    def test_get_one_category(self):
        """
        """
        mgmt = self._get_resource_mgmt()
        expected_category = next(mgmt.list_page(1))
        expected_category_key = expected_category.key
        category = mgmt.get(expected_category_key)
        self.assertIsNotNone(category)
        self.assertEquals(expected_category_key, category.key)

    def test_get_not_existing_category(self):
        """
        """
        mgmt = self._get_resource_mgmt()
        not_existing_key = "test-test-test-test"
        with self.assertRaises(requests.HTTPError):
            category = mgmt.get(not_existing_key)
