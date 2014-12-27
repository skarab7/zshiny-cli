from shiny_client import base


class BrandManager (base.ApiResource, object):
    """
    """
    def __init__(self):
        """
        """
        self._page_size = 40

    def _to_domain_object(self, json):
        return Brand(json)

    def get_schema(self):
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
