import requests
from shiny_client import base
from shiny_client import base_client
from prettytable import PrettyTable
from shiny_client import base_output

CATEGORY_DEFAULT_FIELDS = ["key", "name", "type", "outlet"]


class CategoryGetOneCommand(base_client.CommandBasicProperties, object):
    """
    """
    def __init__(self):
        super(CategoryGetOneCommand, self).__init__("catalog-get",
                                                    "get a catalog entry",
                                                    "categories",
                                                    CATEGORY_DEFAULT_FIELDS)

    def add_parser_args(self, parser):
        """
        """
        parser.add_argument(self.command_name, action="store",
                            help=self.help_info)

    def perform(self, parsed_args):
        unique_id = getattr(parsed_args, self.command_name)

        cm = base.create_resource_mgmt(CategoryManager, self.endpoint, self.lang, self.is_insecure,
                                       False)

        item = cm.get(unique_id)

        if parsed_args.is_machine_readable:
            output = base_output.get_print_for_item(item, self._fields)
        else:
            output = base_output.get_pretty_table_for_item(item, self._fields)

        return output


class CategoryFindByCommand(base_client.CommandBasicProperties, object):
    """
    """
    def __init__(self):
        super(CategoryFindByCommand, self).__init__("catalog-find",
                                                    "get a catalog entry",
                                                    "categories",
                                                    CATEGORY_DEFAULT_FIELDS)

    def add_parser_args(self, parser):
        """
        """
        parser.add_argument(self.command_name, action="store_true",
                            help=self.help_info)
        for f in CategoryManager.get_filter_fields():
            parser.add_argument("--find-by-" + f["name"], action="store", help=f["help_info"])

    def perform(self, parsed_args):
        find_by_fields = {}
        for f in CategoryManager.get_filter_fields():
            f_name = f["name"]
            v = getattr(parsed_args, "find_by_" + f_name)
            if v is not None:
                find_by_fields[f_name] = v

        cm = base.create_resource_mgmt(CategoryManager, self.endpoint, self.lang, self.is_insecure,
                                       False)

        output = base_output.get_pretty_table(cm.find_by(find_by_fields), self._fields)
        return output


class CategoryShowSchemaCommand(base_client.CommandBasicProperties, object):
    """
    """

    def __init__(self):
        super(CategoryShowSchemaCommand, self).__init__("catalog-show-schema",
                                                        "show catalog entry schema",
                                                        "categories",
                                                        CATEGORY_DEFAULT_FIELDS)

    def add_parser_args(self, parser):
        """
        """
        parser.add_argument(self.command_name, action="store_true",
                            help=self.help_info)

    def perform(self, parsed_args):
        output = base_output.get_pretty_json(CategoryManager.get_schema())
        return output


class CategoryStatsCommand(base_client.CommandBasicProperties, object):

    def __init__(self):
        super(CategoryListCommand, self).__init__("catalog-stats",
                                                  "stats of category resource",
                                                  "categories",
                                                  "All")

    def add_parser_args(self, parser):
        """
        """
        parser.add_argument(self.command_name, action="store_true",
                            help=self.help_info)

    def perform(self, parsed_args):
        """
        """
        return "Not implemented!"


class CategoryListCommand(base_client.CommandBasicProperties, object):
    """
    """
    def __init__(self):
        super(CategoryListCommand, self).__init__("catalog-list",
                                                  "list all categories",
                                                  "categories",
                                                  CATEGORY_DEFAULT_FIELDS)

    def add_parser_args(self, parser):
        """
        """
        parser.add_argument(self.command_name, action="store_true",
                            help=self.help_info)

    def perform(self, parsed_args):
        """
        """
        cm = base.create_resource_mgmt(CategoryManager, self.endpoint, self.lang, self.is_insecure,
                                       False)

        output = base_output.get_pretty_table(cm.list(), self._fields)
        return output


class CategoryManager(base.ApiResource, object):
    """
    - find_by,\
      see https://github.com/zalando/shop-api-documentation/wiki/Categories#get-all-categories
    """
    def __init__(self):
        """
        """
        self._page_size = 1000

    def _to_domain_object(self, json):
        return Category(json)

    @staticmethod
    def get_filter_fields():
        """
        TODO: Address the fact that it duplicates the info in json schema:
          - most of the help msg
          - the type
        """

        filter_fields = [{"name":"name", "type": "string", "help_info":"Filters categories by its name containing the given string (ignoring case)"},
                         {"name":"type", "type":"string", "help_info":"Filters categories by its type containing the given string (ignoring case)"},
                         {"name":"outlet", "type":"boolean", "help_info":"Filters outlet categories"},
                         {"name":"hidden", "type": "boolean", "help_info":"Filters hidden categories"},
                         {"name":"targetGroup", "type": "enum", "help_info":"Filters categories matching the given tragetGroup (all, women, men, kids)"}]
        return filter_fields

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
