# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['dsk']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.8.3,<4.0.0',
 'numpy>=1.26.4,<2.0.0',
 'pandas>=2.2.1,<3.0.0',
 'scikit-learn>=1.4.1,<2.0.0',
 'scipy>=1.12.0,<2.0.0',
 'seaborn>=0.13.2,<0.14.0']

setup_kwargs = {
    'name': 'dsk',
    'version': '0.1.0',
    'description': 'A comprehensive toolkit for various data science tasks',
    'long_description': None,
    'author': 'Kristoffer',
    'author_email': 'krg@2021.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
