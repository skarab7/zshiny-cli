import abc


class PluginClientBase(metaclass=abc.ABCMeta):
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
