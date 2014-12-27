from shiny_client import base


class FilterManager(base.SimpleApiResource):
    """
    """
    def _to_domain_object(self, json):
        return Filter(json)

    def get_schema(self):
        return """
        """


class ArticleFilter(base.ApiObject, object):
    """
    """
