from shiny_client import base
from shiny_client import base_client
from shiny_client import base_output

BRAND_DEFAULT_FIELDS = ["key", "name", "brandFamily", "logoUrl"]
BRAND_PAGE_SIZE = 200


class BrandGetOneCommand(base_client.CommandBasicProperties, object):
    """
    """
    def __init__(self):
        super(BrandGetOneCommand, self).__init__("brand-get",
                                                 "get a brand item",
                                                 "brands",
                                                 BRAND_DEFAULT_FIELDS)

    def add_parser_args(self, parser):
        """
        """
        parser.add_argument(self.command_name, action="store",
                            help=self.help_info)

    def perform(self, parsed_args):
        unique_id = getattr(parsed_args, self.command_name)

        cm = base.create_resource_mgmt(BrandManager, self.endpoint, self.lang,
                                       self.is_insecure,
                                       False)

        item = cm.get(unique_id)
        self._print_item(parsed_args, item)

    def _print_item(self, parsed_args, item):
        """
        A separated function that can be overwritten in the tests to not print out
        """
        base_output.print_item(parsed_args, item, self._fields)


class BrandShowSchemaCommand(base_client.CommandBasicProperties, object):
    """
    """

    def __init__(self):
        super(BrandShowSchemaCommand, self).__init__("brand-show-schema",
                                                     "show brand json schema",
                                                     "brands",
                                                     BRAND_DEFAULT_FIELDS)

    def add_parser_args(self, parser):
        """
        """
        parser.add_argument(self.command_name, action="store_true",
                            help=self.help_info)

    def perform(self, parsed_args):
        output = base_output.get_pretty_json(BrandManager.get_schema())
        print(output)


class BrandStatsCommand(base_client.CommandBasicProperties, object):

    def __init__(self):
        super(BrandStatsCommand, self).__init__("brand-stats",
                                                "stats of brand resource",
                                                "brands",
                                                ["totalElements"])

    def add_parser_args(self, parser):
        """
        """
        parser.add_argument(self.command_name, action="store_true",
                            help=self.help_info)

    def perform(self, parsed_args):
        """
        """
        cm = base.create_resource_mgmt(BrandManager, self.endpoint, self.lang, self.is_insecure,
                                       False)
        printed_stats = dict((k, v) for k, v in cm.get_stats().items() if k in self._fields)

        base_output.print_stats(parsed_args, printed_stats)


class BrandListCommand(base_client.CommandBasicProperties, object):
    """
    """
    def __init__(self):
        super(BrandListCommand, self).__init__("brand-list",
                                               "list all brands",
                                               "brands",
                                               BRAND_DEFAULT_FIELDS)

    def add_parser_args(self, parser):
        """
        """
        parser.add_argument(self.command_name, action="store_true",
                            help=self.help_info)

    def perform(self, parsed_args):
        """
        """
        cm = base.create_resource_mgmt(BrandManager, self.endpoint, self.lang, self.is_insecure,
                                       False)

        self._print_list(parsed_args, cm.list())

    def _print_list(self, parsed_args, items):
        base_output.print_list(parsed_args, items, self._fields)


class BrandManager (base.ApiResource, object):
    """
    """
    def __init__(self):
        """
        """
        self._page_size = BRAND_PAGE_SIZE

    def _to_domain_object(self, json):
        return Brand(json)

    @staticmethod
    def get_schema():
        return """
{
    "$$schema": "http://json-schema.org/draft-04/schema#",
    "title" : "Brand",
    "type" : "object",

    "properties" : {
        "key" : {
            "type" : "string",
            "description" : "id"
        },
        "name" : {
            "type" : "string",
            "description" : "human readable name"
        },
        "logoUrl" : {
            "type" : "string",
            "description" : "logo url"
        },
        "shopUrl" : {
            "type" : "string",
            "description" : "shop url"
        },
        "brandFamily" : {
            "type" : "object",
            "description" : "brand family gathers specific brands"
        }
    },
    "required": ["name", "key"],
    "additionalProperties": true
}
        """


class Brand(base.ApiObject, object):
    """
    """
    def get_uuid(self):
        return self.key
