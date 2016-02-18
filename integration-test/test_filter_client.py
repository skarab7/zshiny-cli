import unittest
from shiny_client import article_filter
from base_test import SimpleApiResourceTest


class TestFilterClient(SimpleApiResourceTest, unittest.TestCase):

    RESOURCE_URL = "https://api.zalando.com/filters"

    def _assert_resouce_list_test(self, o):
        self.assertIsNotNone(o.name)

    def _create_resource_mgmt(self):
        return article_filter.FilterManager()

    def _get_resource_endpoint(self):
        return TestFilterClient.RESOURCE_URL
