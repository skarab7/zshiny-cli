import requests
import argparse
import os


ZALANDO_ENDPOINT = os.environ.get("ZALANDO_API_ENDPOINT",
                                  "https://api.zalando.com")


class Client(object):

    # let's discover
    def discover_resources(self, endpoint):
        r = requests.get(endpoint)
        print("ww")
        print(r.json())


class Cli(object):

    def __init__(self):
        self.parser = argparse.ArgumentParser(description='')

    """
    Notes: remember about bash-completion
    """
    def add_general_options_parser(self):
        """
        support for:
          - --insecure - for testing without valid https certs
          -  --za-cacert  - ca certificate // NOT IMPLEMENTED
          - --endpoints
          - --debug flag
          - --lang=
        """
        self.parser.add_argument('--insecure',
                                 action='store_true',
                                 dest="is_insecure",
                                 default=False)
        self.parser.add_argument('--endpoint',
                                 dest="endpoint",
                                 default=ZALANDO_ENDPOINT
                                 )
        self.parser.add_argument('--debug',
                                 action='store_true',
                                 dest="is_debug_enabled")
        self.parser.add_argument('--lang',
                                 dest="lang")

        # for the bash lovers, machine readbale output
        # self.parser.add_argument('--machine-readable ')

    def add_command_parser(self):
        """
        brand-list
        brand-show
        article-list
        article-show
        category-list
        category-show
        """

        artifacts = ["brand", "article", "category"]

        cmds = {"list": "store_true", "show": "store"}

        subparsers = self.parser.add_subparsers(help='commands')

        for art in artifacts:
            for action, store in cmds.items():
                cmd = "{0}-{1}".format(art, action)
                help = ("{0}-{1}".format(art, action)).title()
                subp = subparsers.add_parser(cmd, help=help)
                subp.add_argument(cmd, action=store)

    def add_known_cmd_options_parser(self):
        # filds separated by |
        # so you can customize the output
        self.parser.add_argument('--fields',
                                 dest="fields")

    def get_unknown_args_parser(self):
        """
        The client should be level3, so we should get as much as possible information
        from the http endpoint to make the CLI survive small API changes.
        We should use hypermedia.

        http://martinfowler.com/articles/richardsonMaturityModel.html

        The unknown should be prefixed by 'by-'
        """

    def parse_args(self):
        """
        Parse arguments
        """
        return self.parser.parse_args()


if __name__ == "__main__":
    """
    """
    cli = Cli()
    cli.add_general_options_parser()
    cli.add_command_parser()
    cli.add_known_cmd_options_parser()
    args = cli.parse_args()
