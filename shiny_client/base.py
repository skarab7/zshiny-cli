import requests
import math
from requests_futures.sessions import FuturesSession
from concurrent.futures import ThreadPoolExecutor


def create_resource_mgmt(cls, endpoint, lang, is_insecure, is_debug_enabled):
    mgmt = cls()
    mgmt.resource_url = endpoint
    mgmt.api_lang = lang
    return mgmt


class BaseApiResource(object):
    """
    """
    @property
    def resource_url(self):
        return self._resource_url

    @resource_url.setter
    def resource_url(self, value):
        self._resource_url = value

    @property
    def api_lang(self):
        return self._api_lang

    @api_lang.setter
    def api_lang(self, value):
        self._api_lang = value

    def _do_request(self, args):
        return self._do_request_url(self._resource_url, args)

    def _request_raise_for_status(func):
        def func_wrapper(*args, **kwargs):
                r = func(*args, **kwargs)
                if r.status_code == requests.codes.ok:
                    return r
                else:
                    r.raise_for_status()
        return func_wrapper

    @_request_raise_for_status
    def _do_request_url(self, url, args={}):
        self._apply_lang(args)
        r = requests.get(url, **args)
        return r

    def _apply_lang(self, args):
        if self._api_lang:
            args["headers"] = {"Accept-Language": self._api_lang}


class SimpleApiResource(BaseApiResource):
    """
    """

    def list(self):
        """
        """
        r = self._do_request_url(self._resource_url)
        cs = self._get_object_array_json(r)
        for c in cs:
            yield self._to_domain_object(c)

    def _get_object_array_json(self, r):
        return r.json()


class ApiResource(BaseApiResource):
    """
    A mix-in requires from the base
    class to implement *_to_domain_object*.
    """
    PAGE_SIZE_ATTR = "size"
    PAGE_NUMBER_ATTR = "page"
    TOTAL_NUMBER_ATTR = "totalElements"
    TOTAL_NUMER_PAGES_ATTR = "totalPages"
    REQ_ATTR_PAGE_SIZE = "pageSize"
    REQ_ATTR_PAGE_NUMBER = "page"

    @property
    def page_size(self):
        return self._page_size

    @page_size.setter
    def page_size(self, value):
        self._page_size = value

    def get_stats(self, params={}):
        page_size = 1
        r = self._sync_do_paged_request(1, page_size, params)
        rj = r.json()
        result = {}
        for info in [ApiResource.TOTAL_NUMBER_ATTR, ApiResource.TOTAL_NUMER_PAGES_ATTR,
                     ApiResource.PAGE_NUMBER_ATTR, ApiResource.PAGE_SIZE_ATTR]:
            result[info] = rj[info]
        return result

    def list(self, params={}):
        """
        """
        stats = self.get_stats(params)
        total_pages = math.ceil(stats[ApiResource.TOTAL_NUMBER_ATTR]/self._page_size)
        f = []
        page_num = 1
        num_of_exectors = 3
        session = FuturesSession(executor=ThreadPoolExecutor(max_workers=num_of_exectors))
        #
        # initialize the connections
        #
        for i in range(0, num_of_exectors):
            if page_num > total_pages:
                break
            f_r = self._async_do_paged_request(session, page_num, params)
            f.append(f_r)
            page_num = page_num + 1

        #
        # Harvesting, keep order
        #
        j = 0
        while page_num <= total_pages:
            f_r = f[j % num_of_exectors]
            if f_r:
                r = f_r.result()
                rj = r.json()
                cs = rj["content"]
                for c in cs:
                    yield self._to_domain_object(c)
                f[j % num_of_exectors] = None
            f[j % num_of_exectors] = self._async_do_paged_request(session, page_num, params)
            j = j + 1
            page_num = page_num + 1

        #
        # wait for the all requests to be completed
        #
        for i in range(0, num_of_exectors):
            f_r = f[j % num_of_exectors]
            if f_r:
                r = f_r.result()
                rj = r.json()
                cs = rj["content"]
                for c in cs:
                    yield self._to_domain_object(c)
                f[j % num_of_exectors] = None
            j = j + 1

    def _get_paged_request_args(self, page_num, page_size, args={}):
        paged_args = self._get_args_for_paging(page_num, page_size)
        if args:
            paged_args["params"].update(args)
        return paged_args

    def _get_args_for_paging(self, page_num, page_size):
        result = {"params": {}}
        result["params"][ApiResource.REQ_ATTR_PAGE_SIZE] = page_size
        result["params"][ApiResource.REQ_ATTR_PAGE_NUMBER] = page_num
        return result

    def _async_do_paged_request(self, session, page_num, params):
        args = self._get_paged_request_args(page_num, self._page_size, params)
        self._apply_lang(args)
        return session.get(self._resource_url, **args)

    def _sync_do_paged_request(self, page_num, page_size, args={}):
        paged_args = self._get_paged_request_args(page_num, page_size, args)
        return self._do_request(paged_args)

    def list_page(self, page_num, params={}):
        r = self._sync_do_paged_request(page_num, self._page_size, params)
        rj = r.json()
        cs = rj["content"]

        for c in cs:
            yield self._to_domain_object(c)

    def find_by(self, key_value):
        filter_params = key_value
        return self.list(filter_params)

    def get(self, key):
        """
        """
        url = "{0}/{1}".format(self._resource_url, key)
        r = self._do_request_url(url)
        return self._to_domain_object(r.json())

    def _get_object_array_json(self, r):
        return r.json()["content"]


class ApiObject:
    """
    """
    _req = None

    def __init__(self, req):
        """
        """
        self._req = req

    def __getattribute__(self, attr):
        try:
            return object.__getattribute__(self, attr)
        except AttributeError:
            if attr in self._req:
                return self._req[attr]
            else:
                return None

    def get_attributes(self):
        return self._req.keys()
