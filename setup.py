try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Zalando CLI that works on Zalando API',
    'author': 'Wojciech Barczynski',
    'url': 'URL to get it at.',
    'download_url': '',
    'author_email': 'wpjtek@yahoo.com',
    'version': '0.1',
    'install_requires': ['requests', 'argparse', 'simplejson'],
    'scripts': [],
    'packages': ['shiny_client'],
    'name': 'shiny_client',
    'entry_points': {
        'console_scripts': [
            'zshiny = shiny_client.client:main'
        ]
    }
}
setup(**config)
