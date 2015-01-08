from shiny_client import base
from shiny_client import base_client
from shiny_client import base_output

ARTICLE_DEFAULT_FIELDS = ["name", "id", "model-id", "color", "genders"]


class ArticleGetOneCommand(base_client.CommandBasicProperties, object):
    """
    """
    def __init__(self):
        super(ArticleGetOneCommand, self).__init__("article-get",
                                                   "get a article entry",
                                                   "articles",
                                                   ARTICLE_DEFAULT_FIELDS)

    def add_parser_args(self, parser):
        """
        """
        parser.add_argument(self.command_name, action="store",
                            help=self.help_info)

    def perform(self, parsed_args):
        unique_id = getattr(parsed_args, self.command_name)

        cm = base.create_resource_mgmt(ArticleManager, self.endpoint, self.lang, self.is_insecure,
                                       False)

        item = cm.get(unique_id)
        self._print_item(parsed_args, item)

    def _print_item(self, parsed_args, item):
        """
        A separated function that can be overwritten in the tests to not print out
        """
        base_output.print_item(parsed_args, item, self._fields)


class ArticleFindByFilterCommand(base_client.CommandBasicProperties, object):
    """
    """
    def __init__(self):
        super(ArticleFindByFilterCommand, self).__init__(
            "article-find-by-filter",
            "find using article filters (check: article filter-list).",
            "articles",
            ARTICLE_DEFAULT_FIELDS)

    def add_parser_args(self, parser):
        """
        """
        parser.add_argument(self.command_name, action="store_true",
                            help=self.help_info)

        parser.add_argument("--filter-values", action="store", nargs='+',
                            help="""A list of <filter name : filter value> separated by comma. \
Check the available filter names and possible values with \
article filter-list command.""")

    def perform(self, parsed_args):
        print(parsed_args)

        find_by_filter = {}
        for fv in parsed_args.filter_values:
            separator_pos = fv.find(":")
            fn = fv[0:separator_pos]
            fv = fv[separator_pos + 1:]
            find_by_filter[fn] = fv
        cm = base.create_resource_mgmt(ArticleManager, self.endpoint, self.lang, self.is_insecure,
                                       False)

        base_output.print_list(parsed_args, cm.find_by(find_by_filter), self._fields)

    def _print_list(self, parsed_args, items):
        base_output.print_list(parsed_args, items, self._fields)


class ArticleShowSchemaCommand(base_client.CommandBasicProperties, object):
    """
    """

    def __init__(self):
        super(ArticleShowSchemaCommand, self).__init__("article-show-schema",
                                                       "show article entry schema",
                                                       "articles",
                                                       ARTICLE_DEFAULT_FIELDS)

    def add_parser_args(self, parser):
        """
        """
        parser.add_argument(self.command_name, action="store_true",
                            help=self.help_info)

    def perform(self, parsed_args):
        output = base_output.get_pretty_json(ArticleManager.get_schema())
        print(output)


class ArticleStatsCommand(base_client.CommandBasicProperties, object):

    def __init__(self):
        super(ArticleStatsCommand, self).__init__("article-stats",
                                                  "stats of article resource",
                                                  "articles",
                                                  ["totalElements"])

    def add_parser_args(self, parser):
        """
        """
        parser.add_argument(self.command_name, action="store_true",
                            help=self.help_info)

    def perform(self, parsed_args):
        """
        """
        cm = base.create_resource_mgmt(ArticleManager, self.endpoint, self.lang, self.is_insecure,
                                       False)
        printed_stats = dict((k, v) for k, v in cm.get_stats().items() if k in self._fields)

        base_output.print_stats(parsed_args, printed_stats)


class ArticleListCommand(base_client.CommandBasicProperties, object):
    """
    """
    def __init__(self):
        super(ArticleListCommand, self).__init__("article-list",
                                                 "list all articles",
                                                 "articles",
                                                 ARTICLE_DEFAULT_FIELDS)

    def add_parser_args(self, parser):
        """
        """
        parser.add_argument(self.command_name, action="store_true",
                            help=self.help_info)

    def perform(self, parsed_args):
        """
        """
        print(self.endpoint)
        cm = base.create_resource_mgmt(ArticleManager, self.endpoint, self.lang, self.is_insecure,
                                       False)

        self._print_list(parsed_args, cm.list())

    def _print_list(self, parsed_args, items):
        base_output.print_list(parsed_args, items, self._fields)


class ArticleManager (base.ApiResource, object):
    """
    """
    def __init__(self):
        """
        """
        self._page_size = 200

    def _to_domain_object(self, json):
        return Article(json)

    def search(self, string_query):
        return self.find_by({"fullText": string_query})

    def get_sort_options(self):
        """
        The description from:
        https://github.com/zalando/shop-api-documentation/wiki/Articles#sorting
        In the next version, the options could be extracted from docs (not very good but handy).
        Maybe, zalando will provide a REST where you can get all the sorting options.
        """
        return {"popularity": "sort by popularity (default)",
                "activationDate": "sort articles by their activation date",
                "priceDesc": "expensive articles comes first",
                "priceAsc": "cheaper articles comes first",
                "sale":  "articles on sale comes first"}

    def get_sort_param(self):
        return "sort"

    @staticmethod
    def get_schema():
        """
        The properties dsc were
        taken from Zalando official API docs
        """
        return """
{
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title" : "Article",
    "type" : "object",

    "properties" : {
        "name" : {
            "type" : "string",
            "description" : "human readable name of the category"
        },
        "id" : {
            "type" : "string",
            "description" : "Unique id"
        },
        "modelId" : {
            "type" : "string",
            "description" : "Model unique id"
        },
        "color" : {
            "type" : "string",
            "description" : ""
        },
        "genders" : {
            "type" : "array",
            "description" : ""
        },
        "ageGroups" : {
            "type" : "array",
            "description" : ""
        },
        "available" : {
            "type": "boolean",
            "description" : ""
        },
        "shopUrl" : {
            "type" : "string",
            "description" : ""
        },
        "season" : {
            "type" : "string",
            "description" : ""
        },
        "seasonYear" : {
            "pattern" : "([0-9]{4})|([0-9]{2})|(ALL)",
            "description" : ""
        },
        "brand" : {
            "type" : "object",
            "description" : "Brand, see the *brand* resource"
        },
        "categoryKeys" : {
            "type" : "array",
            "items": {
                "type": "string"
            },
            "uniqueItems": true,
            "description" : "Category, see the *category* resource"
        }
    },
    "required": ["name",
                 "id",
                 "genders",
                 "ageGroups",
                 "brand",
                 "available",
                 "categoryKeys"],
    "additionalProperties": true
}
"""


class Article(base.ApiObject, object):
    """
    """
    def get_uuid(self):
        return self.id
