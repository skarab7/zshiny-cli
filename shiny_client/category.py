import requests
from shiny_client import base
from shiny_client import base_client


class CategoryListCommand(object):
    """
    """

    cmd = "catalog-list"
    help_info = ""
    _resource_name = "categories"

    @property
    def endpoint(self):
        return self._endpoint

    @endpoint.setter
    def endpoint(self, value):
        self._endpoint = value

    @property
    def lang(self):
        return self._lang

    @lang.setter
    def lang(self, value):
        self._lang = value

    @property
    def is_insecure(self):
        return self._is_insecure

    @is_insecure.setter
    def is_insecure(self, value):
        self._is_insecure = value

    @property
    def fields(self):
        return self._fields

    @fields.setter
    def fields(self, value):
        self._fields = value

    @property
    def command_name(self):
        return CategoryListCommand.cmd

    @property
    def help_info(self):
        return CategoryListCommand.help_info

    @property
    def resource_name(self):
        return CategoryListCommand._resource_name

    def add_parser_args(self, parser):
        """
        """
        parser.add_argument(CategoryListCommand.cmd, action="store_true",
                            help="List all the categories")

    def perform(self, parsed_args):
        """
        """
        cm = base.create_resource_mgmt(CategoryManager, self.endpoint, self.lang, self.is_insecure,
                                       False)

        fields = base_client.get_required_attributes(parsed_args)

        for c in cm.list_page(1):
            output = ""
            for attr in c.get_attributes():
                if not fields or attr in fields:
                    output = output + "|{0}:{1}".format(attr, getattr(c, attr))
            print(output)

    def show_schema(self):
        return CategoryManager.get_schema()


class CategoryManager(base.ApiResource, object):
    """
    - find_by,\
      see https://github.com/zalando/shop-api-documentation/wiki/Categories#get-all-categories
    """
    def __init__(self):
        """
        """
        self._page_size = 40

    def _to_domain_object(self, json):
        return Category(json)

    @staticmethod
    def get_schema():
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


class Category(base.ApiObject, object):
    """
    """
    def get_uuid(self):
        return self.key
