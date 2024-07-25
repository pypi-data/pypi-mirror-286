# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fmd']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.7.2,<0.8.0', 'requests>=2.32.3,<3.0.0']

setup_kwargs = {
    'name': 'fmd',
    'version': '0.1.0',
    'description': 'Provide users with an easy-to-use interface to access data from the FMD API.',
    'long_description': '# fmd\n\nProvide users with an easy-to-use interface to access data from the FMD API.',
    'author': 'Yu Chen, Yang',
    'author_email': 'ycy.tai@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
