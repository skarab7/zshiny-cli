from shiny_client import base


class ResourceEndpointManager(base.SimpleApiResource):
    """
    """

    def _to_domain_object(self, json):
        return ResourceEndpoint(json["resources"])

    def _get_object_array_json(self, r):
        return [r.json()]


class ResourceEndpoint(base.ApiObject, object):
    """
    """
    # @property
    # def resource_url(self):
    #    return self._req.values()[0]
    # @property
    # def resource_name(self):
    #    return self._req.keys()[0]
    def find_resource_url(self, resource_name):
        return self._req[resource_name]
