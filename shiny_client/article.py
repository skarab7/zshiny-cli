from shiny_client import base
from shiny_client import base_client
from shiny_client import base_output

ARTICLE_DEFAULT_FIELDS = ["name", "id", "model-id", "color", "genders"]


def add_support_for_sorting(parser):
    for so in ArticleManager.get_sort_options():
        parser.add_argument("--sort-by-" + so["name"], action="store_true", help=so["help_info"])


def add_soring_args_to_params(args, params):
    param_name = ArticleManager.get_sort_param()

    for so in ArticleManager.get_sort_options():
        attr_name = "sort_by_" + so["name"].replace("-", "_")
        v = getattr(args, attr_name)
        if v:
            params[param_name] = so["name"]
            break


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


class ArticleFullTextSearchCommand(base_client.CommandBasicProperties, object):
    """
    """
    def __init__(self):
        super(ArticleFullTextSearchCommand, self).__init__(
            "article-search",
            "full-text search for articles",
            "articles",
            ARTICLE_DEFAULT_FIELDS)

    def add_parser_args(self, parser):
        """
        """
        parser.add_argument(self.command_name, action="store",
                            help=self.help_info)
        add_support_for_sorting(parser)

    def perform(self, parsed_args):
        text_query = getattr(parsed_args, self.command_name)

        params = {}
        add_soring_args_to_params(parsed_args, params)

        cm = base.create_resource_mgmt(ArticleManager, self.endpoint, self.lang, self.is_insecure,
                                       False)
        base_output.print_list(parsed_args, cm.search(text_query, params), self._fields)

    def _print_list(self, parsed_args, items):
        base_output.print_list(parsed_args, items, self._fields)


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
                            help="""A list of <filter name : filter value> separated by space. \
Check the available filter names and possible values with \
article filter-list command.""")
        add_support_for_sorting(parser)

    def perform(self, parsed_args):
        find_by_filter = {}
        for fv in parsed_args.filter_values:
            separator_pos = fv.find(":")
            fn = fv[0:separator_pos]
            fv = fv[separator_pos + 1:]
            if fn not in find_by_filter:
                find_by_filter[fn] = []
            find_by_filter[fn].append(fv)

        add_soring_args_to_params(parsed_args, find_by_filter)

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
        add_support_for_sorting(parser)

    def perform(self, parsed_args):
        """
        """
        params = {}
        add_soring_args_to_params(parsed_args, params)
        cm = base.create_resource_mgmt(ArticleManager, self.endpoint, self.lang, self.is_insecure,
                                       False)
        self._print_list(parsed_args, cm.list(params))

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

    def search(self, string_query, params={}):
        params["fullText"] = string_query
        return self.find_by(params)

    @staticmethod
    def get_sort_options():
        """
        The description from:
        https://github.com/zalando/shop-api-documentation/wiki/Articles#sorting
        In the next version, the options could be extracted from docs (not very good but handy).
        Maybe, zalando will provide a REST where you can get all the sorting options.
        """
        return [{"name": "popularity", "help_info": "sort by popularity (default)"},
                {"name": "activationDate", "help_info": "sort articles by their activation date"},
                {"name": "priceDesc", "help_info": "expensive articles comes first"},
                {"name": "priceAsc", "help_info": "cheaper articles comes first"},
                {"name": "sale", "help_info": "articles on sale comes first"}]

    @staticmethod
    def get_sort_param():
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
