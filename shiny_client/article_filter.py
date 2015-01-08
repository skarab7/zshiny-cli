from shiny_client import base
from shiny_client import base_client
from shiny_client import base_output


FILTER_DEFAULT_FIELDS = ["name", "type", "multiValue"]


class FilterGetOneCommand(base_client.CommandBasicProperties, object):
    """
    """
    def __init__(self):
        super(FilterGetOneCommand, self).__init__("filter-get",
                                                  "get a filter entry",
                                                  "filters",
                                                  "all")

    def add_parser_args(self, parser):
        """
        """
        parser.add_argument(self.command_name, action="store",
                            help=self.help_info)

    def perform(self, parsed_args):
        unique_id = getattr(parsed_args, self.command_name)

        cm = base.create_resource_mgmt(FilterManager, self.endpoint, self.lang, self.is_insecure,
                                       False)

        items = (i for i in cm.list() if i.name == unique_id)
        items = list(items)
        self._print_item(parsed_args, items[0])

    def _print_item(self, parsed_args, item):
        """
        A separated function that can be overwritten in the tests to not print out
        """
        base_output.print_item(parsed_args, item, self._fields)


class FilterShowSchemaCommand(base_client.CommandBasicProperties, object):
    """
    """

    def __init__(self):
        super(FilterShowSchemaCommand, self).__init__("filter-show-schema",
                                                      "show filter entry schema",
                                                      "filters",
                                                      FILTER_DEFAULT_FIELDS)

    def add_parser_args(self, parser):
        """
        """
        parser.add_argument(self.command_name, action="store_true",
                            help=self.help_info)

    def perform(self, parsed_args):
        output = base_output.get_pretty_json(FilterManager.get_schema())
        print(output)


class FilterListCommand(base_client.CommandBasicProperties, object):
    """
    """
    def __init__(self):
        super(FilterListCommand, self).__init__("filter-list",
                                                "list all article filters",
                                                "filters",
                                                FILTER_DEFAULT_FIELDS)

    def add_parser_args(self, parser):
        """
        """
        parser.add_argument(self.command_name, action="store_true",
                            help=self.help_info)

    def perform(self, parsed_args):
        """
        """
        print(self.endpoint)
        cm = base.create_resource_mgmt(FilterManager, self.endpoint, self.lang, self.is_insecure,
                                       False)

        self._print_list(parsed_args, cm.list())

    def _print_list(self, parsed_args, items):
        base_output.print_list(parsed_args, items, self._fields)


class FilterManager(base.SimpleApiResource):
    """
    """

    def _to_domain_object(self, json):
        return ArticleFilter(json)

    @staticmethod
    def get_schema():
        f = ")|(".join(FilterManager.get_filter_types())
        filter_type_pattern = "(" + f + ")"
        return """
{
    "$$schema": "http://json-schema.org/draft-04/schema#",
    "title" : "Filter",
    "type" : "object",

    "properties" : {
        "name" : {
            "type" : "string",
            "description" : "human readable name"
        },
        "type": {
            "pattern" : "%s",
            "description" : "see "
        }
    },
    "required": ["name"],
    "additionalProperties": true
}
""" % (filter_type_pattern)

    @staticmethod
    def get_filter_types():
        return ["enum", "key", "range", "string"]


class ArticleFilter(base.ApiObject, object):
    """
    """
