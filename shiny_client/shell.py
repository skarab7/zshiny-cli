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

    def add_enabled_commands(self, resource_clients):
        self._discover_enabled_commands(resource_clients)
        self._add_commands_parser_args()

    def _discover_enabled_commands(self, resource_clients):
        for cls in resource_clients:
            cmd = cls()
            self.clients[cmd.command_name] = cmd

    def _add_commands_parser_args(self):

        subparsers = self.parser.add_subparsers(dest='subparser_name')

        for k, c in self.clients.items():
            cn = c.command_name
            ch = c.help_info
            subp = subparsers.add_parser(cn, help=ch)
            c.add_parser_args(parser=subp)
            self._add_connection_args(subp)
            self._add_output_options_args(subp)

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

    def parse_args(self):
        """
        Parse arguments
        """
        self._args = self.parser.parse_args()

    def get_parsed_args(self):
        return self._args

    def print_parser_help_msg(self):
        return self.parser.print_help()

    def execute_command(self, resource_catalog):
        cmd = self.clients[self._args.subparser_name]
        cmd.lang = self._args.lang
        cmd.endpoint = get_resource_url(cmd, resource_catalog)
        cmd.is_insecure = False
        if self._args.output_fields:
            cmd.fields = self._args.output_fields
        cmd.perform(self._args)


def get_resource_url(cmd, resource_catalog):
    result = resource_catalog.find_resource_url(cmd.resource_name)
    return result


def get_resource_catalog(args):
    rm = create_resource_mgmt(ResourceEndpointManager, args.endpoint,
                              args.lang, args.is_insecure, args.is_debug_enabled)
    result = list(rm.list())[0]
    return result


def is_any_parser_matched(args):
    return args.subparser_name is not None


def main():
    """
    """
    cli = Cli()
    cli.add_enabled_commands(clients.enabled_commands)
    cli.parse_args()
    parsed_args = cli.get_parsed_args()
    if not is_any_parser_matched(parsed_args):
        cli.print_parser_help_msg()
    else:
        resource_catalog = get_resource_catalog(parsed_args)
        cli.execute_command(resource_catalog)

if __name__ == "__main__":
    main()
