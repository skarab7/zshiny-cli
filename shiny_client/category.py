import requests


class CategoryManager:
    """
    """
    def __init__(self):
        """
        """
        self._page_size = 40

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

    def list(self):
        page_num = total_pages = 1

        while page_num <= total_pages:
            r = self._get_paged_request(page_num, self._page_size)
            rj = r.json()
            cs = rj["content"]

            for c in cs:
                yield Category(c)

            page_num = rj["page"] + 1
            total_pages = rj["totalPages"]

    def _get_paged_request(self, page_num, page_size, args={}):
        paged_args = {"params": {"pageSize": page_size, "page": page_num}}
        if args:
            paged_args.update(args)
        return self._do_request(paged_args)

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
        if self._api_lang:
            args["headers"] = {"Accept-Language": self._api_lang}
        r = requests.get(url, **args)
        return r

    def list_page(self, page_num):
        r = self._get_paged_request(page_num, self._page_size)
        rj = r.json()
        cs = rj["content"]

        for c in cs:
            yield Category(c)

    def find_by(self, key_value):
        """
        see https://github.com/zalando/shop-api-documentation/wiki/Categories#get-all-categories
        """
        filter_params = {"params": key_value}
        page_num = total_pages = 1

        while page_num <= total_pages:
            r = self._get_paged_request(page_num, self._page_size, filter_params)
            rj = r.json()
            cs = rj["content"]

            for c in cs:
                yield Category(c)

            page_num = rj["page"] + 1
            total_pages = rj["totalPages"]

    def get(self, key):
        """
        """
        url = "{0}/{1}".format(self._resource_url, key)
        r = self._do_request_url(url)
        rj = r.json()
        return Category(rj)

    def get_schema(self):
        """
        The properties dsc were
        taken from Zalando official API docs
        """
        return """
{
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title" : "Catalog",
    "type" : "object",

    "properties" : {
        "name" : {
            "type" : "string",
            "description" : "human readable name of the category"
        },
        "key" : {
            "type" : "string",
            "description" : "the key of the category"
        },
        "parentKey" : {
            "type" : "string",
            "description" : "the key of the parent category of this item"
        },
        "childKeys" : {
            "type" : "array",
            "items": {
                "type": "string"
            },
            "uniqueItems": true,
            "description" :  "keys of subcategories of the category"
        },
        "type" : {
            "type" : "string",
            "description" : "categories with sports and premium assortment"
        },
        "outlet" : {
            "type" : "boolean",
            "description": "categories that contains articles from last seasons"
        },
        "hidden" : {
            "type" : "boolean",
            "description": "category is not visible on web, all articles can be found under parent"
        },
        "targetGroup" : {
            "pattern" : "^(ALL)|(WOMEN)|(MEN)|(KIDS)$",
            "description" : "Filters categories matching the given tragetGroup"
        }
    },
    "required": ["name", "key", "outlet", "targetGroup"],
    "additionalProperties": true
}
"""


class Category(object):

    _req = None

    def __init__(self, req):
        """
        """
        self._req = req
        self.name = req["name"]
        self.key = req["key"]

    def __getattribute__(self, attr):
        try:
            return object.__getattribute__(self, attr)
        except AttributeError:
            if attr in self._req:
                return self._req[attr]
            else:
                return None
