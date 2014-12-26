from shiny_client import base


class ArticleManager (base.ApiResource, object):
    """
    """
    def __init__(self):
        """
        """
        self._page_size = 40

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

    def get_schema(self):
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
