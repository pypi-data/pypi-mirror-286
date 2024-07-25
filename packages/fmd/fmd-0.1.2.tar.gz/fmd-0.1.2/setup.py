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
    'version': '0.1.2',
    'description': 'Provide users with an easy-to-use interface to access data from the FMD API.',
    'long_description': "# fmd\n\nProvides users with an easy-to-use interface to access data from the *Financial Market Data (FMD)* API, specializing in Taiwan's financial markets.\n\n## Installation\n\nInstall via `pip`\n```\npip install fmd\n```\n\n## Quick Start\n\nRetrieve data through `FmdApi` with various predefined methods.\n```python\nfrom fmd import FmdApi\n\nfmd_api = FmdApi()\ndata = fmd_api.get_stock_price(\n    symbol='2330', \n    start_date='2024-07-01', \n    end_date='2024-07-15'\n)\n```\n",
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
