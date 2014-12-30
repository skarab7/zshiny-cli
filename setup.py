import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Zalando CLI that works on Zalando API',
    'license': 'Apache 2',
    'long_description': read('README.rst')
    'author': 'Wojciech Barczynski',
    'url': 'URL to get it at.',
    'download_url': '',
    'author_email': 'wpjtek@yahoo.com',
    'version': '0.1',
    'install_requires': read('requirements.txt'),
    'scripts': [],
    'packages': ['shiny_client'],
    'name': 'shiny_client',
    'entry_points': {
        'console_scripts': [
            'zshiny = shiny_client.client:main'
        ]
    },
    'keywords': "zalando API REST commandline cli"
}
setup(**config)
