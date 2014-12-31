import requests
import argparse
import os
from shiny_client import base_client
from shiny_client.base import create_resource_mgmt
from shiny_client import clients
from shiny_client.discovery_service import ResourceEndpointManager

ZALANDO_ENDPOINT = os.environ.get("ZALANDO_API_ENDPOINT",
                                  "https://api.zalando.com")


class Cli(object):

    def __init__(self):
        self.parser = argparse.ArgumentParser(description='')
        self.clients = dict()

    def add_commands(self, resource_clients):
        for cls in resource_clients:
            cmd = cls()
            self.clients[cmd.command_name] = cmd

    """
    Notes: remember about bash-completion
    """
    def _add_connection_args(self, subparser):
        """
        support for:
          - --insecure - for testing without valid https certs
          -  --za-cacert  - ca certificate // NOT IMPLEMENTED
          - --endpoint
          - --debug flag
          - --lang=
        """
        subparser.add_argument('--insecure',
                               action='store_true',
                               dest="is_insecure",
                               default=False)
        subparser.add_argument('--endpoint',
                               dest="endpoint",
                               default=ZALANDO_ENDPOINT
                               )
        subparser.add_argument('--lang',
                               dest="lang")

    def _add_output_options_args(self, subparser):
        subparser.add_argument('--debug',
                               action='store_true',
                               dest="is_debug_enabled", help="NOT_IMPLEMENTED")
        subparser.add_argument('--machine-readable', action='store_true',
                               dest="is_machine_readable", help="NOT_IMPLEMENTED")
        subparser.add_argument('--fields', action='store', dest="output_fields",
                               help="NOT_IMPLEMENTED", default=None)
        # for the bash lovers, machine readable output
        # self.parser.

    def add_command_parser(self):

        subparsers = self.parser.add_subparsers(dest='subparser_name')

        for k, c in self.clients.items():
            cn = c.command_name
            ch = c.help_info
            subp = subparsers.add_parser(cn, help=ch)
            c.add_parser_args(parser=subp)
            self._add_connection_args(subp)
            self._add_output_options_args(subp)

    def parse_args(self):
        """
        Parse arguments
        """
        return self.parser.parse_args()

    def get_resource_catalog(self, args):
        rm = create_resource_mgmt(ResourceEndpointManager, args.endpoint,
                                  args.lang, args.is_insecure, args.is_debug_enabled)
        result = list(rm.list())[0]
        return result

    def execute_command(self, args, resource_catalog):
        cmd = self.clients[args.subparser_name]
        cmd.lang = args.lang
        cmd.endpoint = self.get_resource_url(cmd, resource_catalog)
        cmd.is_insecure = False
        cmd.perform(args)

    def get_resource_url(self, cmd, resource_catalog):
        result = resource_catalog.find_resource_url(cmd.resource_name)
        return result

        # """
        # brand-list
        # brand-show
        # article-list
        # article-show
        # ategory-list
        # category-show
        # """
        # artifacts = ["brand", "article", "category"]
        # cmds = {"list": "store_true", "show": "store"}
        # for art in artifacts:
        #    for action, store in cmds.items():
        #        cmd = "{0}-{1}".format(art, action)
        #        help = ("{0}-{1}".format(art, action)).title()
        #
        #        subp.add_argument(cmd, action=store)
    # def add_known_cmd_options_parser(self):
    #    # filds separated by |
    #    # so you can customize the output
    #    self.parser.add_argument('--fields',
    #                             dest="fields")

    # def get_unknown_args_parser(self):
    #    """
    #    The client should be level3, so we should get as much as possible information
    #    from the http endpoint to make the CLI survive small API changes.
    #    We should use hypermedia.
    #    http://martinfowler.com/articles/richardsonMaturityModel.html
    #
    #    The unknown should be prefixed by 'by-'
    #    """


if __name__ == "__main__":
    """
    """
    cli = Cli()
    cli.add_commands(clients.enabled_commands)
    cli.add_command_parser()
#    cli.add_known_cmd_options_parser()
    args = cli.parse_args()
    resource_catalog = cli.get_resource_catalog(args)
    cli.execute_command(args, resource_catalog)
