import requests


class CategoryManager:
    """
    """
    def __init__(self):
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

    def list(self):
        r = self._do_request({})
        cs = r.json()["content"]
        for c in cs:
            yield Category(c)

    def _do_request(self, args):
        if self._api_lang:
            args["headers"] = {"Accept-Language": self._api_lang}
        r = requests.get(self._resource_url, **args)
        return r

    def find_by_name(self, name):
        args = {"params": {"name": name}}
        r = self._do_request(args)

    def get(self, key):
        """
        """

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
