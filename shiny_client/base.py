import requests


class ApiResource:
    """
    A mix-in requires from the base
    class to implement *_to_domain_object*.
    """
    PARAMETER_PAGE_SIZE = "size"
    PARAMETER_PAGE_NUMBER = "page"

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

    @property
    def page_size(self):
        return self._page_size

    @page_size.setter
    def page_size(self, value):
        self._page_size = value

    def list(self):
        page_num = total_pages = 1

        while page_num <= total_pages:
            r = self._get_paged_request(page_num, self._page_size)
            rj = r.json()
            cs = rj["content"]

            for c in cs:
                yield self._to_domain_object(c)

            page_num = rj["page"] + 1
            total_pages = rj["totalPages"]

    def _get_paged_request(self, page_num, page_size, args={}):
        paged_args = self._get_args_for_paging(page_num, page_size)
        if args:
            paged_args.update(args)
        return self._do_request(paged_args)

    def _get_args_for_paging(self, page_num, page_size):
        result = {"params": {}}
        result["params"][ApiResource.PARAMETER_PAGE_SIZE] = page_size
        result["params"][ApiResource.PARAMETER_PAGE_NUMBER] = page_num
        return result

    def _do_request(self, args):
        return self._do_request_url(self._resource_url, args)

    def _request_raise_for_status(func):
        def func_wrapper(*args, **kwargs):
                r = func(*args, **kwargs)
                if r.status_code == requests.codes.ok:
                    return r
                else:
                    print(r.url)
                    r.raise_for_status()
        return func_wrapper

    @_request_raise_for_status
    def _do_request_url(self, url, args={}):
        if self._api_lang:
            args["headers"] = {"Accept-Language": self._api_lang}
        r = requests.get(url, **args)
        return r

    def list_page(self, page_num):
        r = self._get_paged_request(page_num, self._page_size)
        rj = r.json()
        cs = rj["content"]

        for c in cs:
            yield self._to_domain_object(c)

    def find_by(self, key_value):
        filter_params = {"params": key_value}
        page_num = total_pages = 1

        while page_num <= total_pages:
            r = self._get_paged_request(page_num, self._page_size, filter_params)
            rj = r.json()
            cs = rj["content"]

            for c in cs:
                yield self._to_domain_object(c)

            page_num = rj["page"] + 1
            total_pages = rj["totalPages"]

    def get(self, key):
        """
        """
        url = "{0}/{1}".format(self._resource_url, key)
        r = self._do_request_url(url)
        return self._to_domain_object(r.json())


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
