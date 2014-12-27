import unittest
from shiny_client import article
import requests
from base_test import ApiResourceTest, SimpleApiResourceTest


class TestArticleClient(ApiResourceTest, unittest.TestCase):

    RESOURCE_URL = "https://api.zalando.com/articles"
    SEARCH_QUERY_STRING = "shoe"

    def _assert_resouce_list_test(self, o):
        self.assertIsNotNone(o.name)
        self.assertIsNotNone(o.get_uuid())
        self.assertIsNotNone(o.id)
        self.assertEquals(o.get_uuid(), o.id)

    def _create_resource_mgmt(self):
        return article.ArticleManager()

    def _get_resource_endpoint(self):
        return TestArticleClient.RESOURCE_URL

    def test_find_by_filtering_attributes(self):
        """
        The valid values can be found:

        https://api.zalando.com/filters
        """
        mgmt = self._get_resource_mgmt()
        query_value = "female"
        query = {"gender": query_value}

        c = next(mgmt.find_by(query))
        self.assertTrue(c.available)
        if query_value not in c.genders and query_value.lower() not in c.genders:
            self.assertTrue("False")

    def test_fulltext_search(self):
        """
        """
        mgmt = self._get_resource_mgmt()
        query_string = TestArticleClient.SEARCH_QUERY_STRING
        c = next(mgmt.search(query_string))
        # TODO: consider redesign of this code fragment
        c_as_string = ""
        for a in c.get_attributes():
            c_as_string = "{0}{1}".format(c_as_string, getattr(c, a))
        self.assertTrue(True)
        self.assertTrue(query_string.lower() in c_as_string.lower())

    def test_sort_by_price_desc(self):
        """
        """
        sort_option = "priceDesc"
        mgmt = self._get_resource_mgmt()
        sort_param = mgmt.get_sort_param()
        all_options = mgmt.get_sort_options()
        self.assertTrue(sort_option in all_options)

        prev_value = 0

        is_first_iteration = True
        for c in mgmt.list_page(2, {"params": {sort_param: sort_option}}):
            if(is_first_iteration):
                is_first_iteration = False
            else:
                self.assertTrue(prev_value >= c.units[0]['price']['value'])
            prev_value = c.units[0]['price']['value']
