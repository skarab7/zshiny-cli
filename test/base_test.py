import os
import jsonschema
import json
import requests


class BaseResourceTest:

    def get_api_lang(self):
        return os.getenv("SHINY_CLIENT_TEST_API_LANG", "pl-PL")

    def _get_resource_mgmt(self):
        mgmt = self._create_resource_mgmt()
        mgmt.resource_url = self._get_resource_endpoint()
        mgmt.api_lang = self.get_api_lang()
        return mgmt

    def test_integration_with_api(self):
        mgmt = self._get_resource_mgmt()
        r = mgmt._do_request({})
        for i in range(10):
            object_as_json = mgmt._get_object_array_json(r)[i]
            js = mgmt.get_schema()
            json_schema = json.loads(js)
            jsonschema.validate(object_as_json, json_schema)


class SimpleApiResourceTest(BaseResourceTest):

    def test_filter_list(self):
        """
        Full list of the resource, only for resources
        that do not support paging
        """
        mgnt = self._get_resource_mgmt()

        for o in mgnt.list():
            self._assert_resouce_list_test(o)


class ApiResourceTest(BaseResourceTest):

    def test_category_manager(self):
        mgmt = self._get_resource_mgmt()

        for o in mgmt.list_page(1):
            self._assert_resouce_list_test(o)

    def test_get_one_object(self):
        """
        """
        mgmt = self._get_resource_mgmt()
        expected_obj = next(mgmt.list_page(1))
        expected_obj_uuid = expected_obj.get_uuid()
        obj = mgmt.get(expected_obj_uuid)
        self.assertIsNotNone(obj)
        self.assertEquals(expected_obj_uuid, obj.get_uuid())

    def test_get_nonexisting(self):
        """
        """
        mgmt = self._get_resource_mgmt()
        not_existing_key = "test-test-test-test"
        with self.assertRaises(requests.HTTPError):
            category = mgmt.get(not_existing_key)


class ApiResourceWithFindTest(ApiResourceTest):
    """
    """
