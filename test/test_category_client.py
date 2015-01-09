import unittest
from shiny_client import category
import requests
from base_test import ApiResourceTest
from shiny_client import base_client


class TestCategoryListCommand(unittest.TestCase):

    RESOURCE_URL = "https://api.zalando.com/categories"

    def test_instantiate(self):
        base_client.PluginCommandBase.register(category.CategoryListCommand)
        c = category.CategoryListCommand()
        self.assertTrue(issubclass(category.CategoryListCommand, base_client.PluginCommandBase))
        self.assertTrue(isinstance(category.CategoryListCommand(), base_client.PluginCommandBase))

    def test_get_list(self):
        c = category.CategoryListCommand()
        c.lang = "EN-en"
        c.endpoint = TestCategoryListCommand.RESOURCE_URL
        c.is_insecure = False
        parsed_args = lambda: None
        parsed_args.fields = ['name', 'key', 'type', 'parentKey']
        parsed_args.is_machine_readable = True
        c.perform(parsed_args)

    def test_show_schema(self):
        c = category.CategoryListCommand()
        # c.show_schema()


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
        query = {"name": "s"}
        stats = mgmt.get_stats(query)
        is_found = 0
        for c in mgmt.find_by(query):
            is_found = is_found + 1

        self.assertEquals(is_found, stats["totalElements"])

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

    def test_get_stats(self):
        mgmt = self._get_resource_mgmt()
        result = mgmt.get_stats()
        self.assertTrue("totalElements" in result)
