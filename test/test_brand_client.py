import unittest
from shiny_client import brand
import requests
from base_test import ApiResourceTest


class TestBrandClient(ApiResourceTest, unittest.TestCase):

    RESOURCE_URL = "https://api.zalando.com/brands"

    def _assert_resouce_list_test(self, o):
        self.assertIsNotNone(o.name)
        self.assertIsNotNone(o.get_uuid())
        self.assertIsNotNone(o.key)
        self.assertEquals(o.get_uuid(), o.key)

    def _create_resource_mgmt(self):
        return brand.BrandManager()

    def _get_resource_endpoint(self):
        return TestBrandClient.RESOURCE_URL
