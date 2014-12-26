import unittest
from shiny_client import client
from shiny_client import article
import jsonschema
import json
import requests
import os


class TestArticleClient(unittest.TestCase):

    API_LANG = os.getenv("SHINY_CLIENT_TEST_API_LANG", "pl-PL")
    RESOURCE_URL = "https://api.zalando.com/articles"
    SEARCH_QUERY_STRING = "shoe"

    @unittest.skip
    def test_article_manager(self):
        mgmt = self._get_article_mgmt()

        for c in mgmt.list_page(2):
            self.assertIsNotNone(c.name)
            self.assertIsNotNone(c.get_uuid())
            self.assertIsNotNone(c.id)
            self.assertEquals(c.get_uuid(), c.id)

    def _get_article_mgmt(self):
        mgmt = article.ArticleManager()
        mgmt.resource_url = TestArticleClient.RESOURCE_URL
        mgmt.api_lang = TestArticleClient.API_LANG
        return mgmt

    @unittest.skip
    def test_integration_with_api(self):
        """
        Check whether the CLI creator understands the API.
        Test against the changes in schema.
        """
        mgmt = self._get_article_mgmt()
        r = mgmt._do_request({})
        for i in range(10):
            object_as_json = r.json()["content"][i]
            js = mgmt.get_schema()
            json_schema = json.loads(js)
            jsonschema.validate(object_as_json, json_schema)

    @unittest.skip
    def test_get_one_object(self):
        """
        """
        mgmt = self._get_article_mgmt()
        expected_obj = next(mgmt.list_page(1))
        expected_obj_uuid = expected_obj.get_uuid()
        obj = mgmt.get(expected_obj_uuid)
        self.assertIsNotNone(obj)
        self.assertEquals(expected_obj_uuid, obj.get_uuid())

    @unittest.skip
    def test_get_nonexisting(self):
        """
        """
        mgmt = self._get_article_mgmt()
        not_existing_key = "test-test-test-test"
        with self.assertRaises(requests.HTTPError):
            category = mgmt.get(not_existing_key)

    def test_find_by_filtering_attributes(self):
        """
        The valid values can be found:

        https://api.zalando.com/filters
        """
        mgmt = self._get_article_mgmt()
        query_value = "female"
        query = {"gender": query_value}

        c = next(mgmt.find_by(query))
        self.assertTrue(c.available)
        if query_value not in c.genders and query_value.lower() not in c.genders:
            self.assertTrue("False")

    def test_fulltext_search(self):
        """
        """
        mgmt = self._get_article_mgmt()
        query_string = TestArticleClient.SEARCH_QUERY_STRING
        c = next(mgmt.search(query_string))
        # TODO: consider redesign of this code fragment
        c_as_string = ""
        for a in c.get_attributes():
            c_as_string = "{0}{1}".format(c_as_string, getattr(c, a))
        self.assertTrue(True)
        self.assertTrue(query_string.lower() in c_as_string.lower())

    # the sorting should be supported for all search / list / find
    def test_sort(self):
        """
        """

