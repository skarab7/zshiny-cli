from shiny_client import base


class FilterManager(base.SimpleApiResource):
    """
    """

    def _to_domain_object(self, json):
        return ArticleFilter(json)

    def get_schema(self):
        f = ")|(".join(self.get_filter_types())
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

    def get_filter_types(self):
        return ["enum", "key", "range", "string"]


class ArticleFilter(base.ApiObject, object):
    """
    """
