import abc
from shiny_client import base


class PluginCommandBase(metaclass=abc.ABCMeta):
    """
    """

    @abc.abstractproperty
    def help_info(self):
        pass

    @abc.abstractproperty
    def command_name():
        pass

    @abc.abstractmethod
    def add_parser_args(self, parser):
        pass


class CommandBasicProperties:

    def __init__(self, cmd_name, help_info, resource_name, fields):
        self._cmd_name = cmd_name
        self._help_info = help_info
        self._resource_name = resource_name
        self._fields = fields

    @property
    def command_name(self):
        return self._cmd_name

    @property
    def help_info(self):
        return self._help_info

    @property
    def resource_name(self):
        return self._resource_name

    @property
    def endpoint(self):
        return self._endpoint

    @endpoint.setter
    def endpoint(self, value):
        self._endpoint = value

    @property
    def lang(self):
        return self._lang

    @lang.setter
    def lang(self, value):
        self._lang = value

    @property
    def is_insecure(self):
        return self._is_insecure

    @is_insecure.setter
    def is_insecure(self, value):
        self._is_insecure = value

    @property
    def fields(self):
        return self._fields

    @fields.setter
    def fields(self, value):
        self._fields = value

    @property
    def request_timeout(self):
        return self._request_timeout

    @request_timeout.setter
    def request_timeout(self, value):
        self._request_timeout = value


def create_resource_mgmt(self, cls):
    return base.create_resource_mgmt(cls,
                                     self.endpoint,
                                     self.lang,
                                     self.request_timeout,
                                     self.is_insecure,
                                     False)
