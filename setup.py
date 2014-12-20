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
    'install_requires': ['click', 'request'],
    'scripts': [],
    'name': 'projectname'
}
setup(**config)
