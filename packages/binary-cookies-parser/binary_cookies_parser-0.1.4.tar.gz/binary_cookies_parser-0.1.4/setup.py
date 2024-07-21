# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['binary_cookies_parser']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=2.8.2,<3.0.0', 'pytest>=8.2.2,<9.0.0', 'typer>=0.12.3,<0.13.0']

entry_points = \
{'console_scripts': ['bcparser = binary_cookies_parser.__main__:main']}

setup_kwargs = {
    'name': 'binary-cookies-parser',
    'version': '0.1.4',
    'description': 'Parses binary cookies from a given .binarycookies file',
    'long_description': '# Binary Cookies Reader\n\nThis project provides a CLI tool to read and interpret binary cookie files.\nThe project is based on the cookie reader written by Satishb3 \n\n## Requirements\n\n- Python 3.8 or higher\n\n## Installation\n```bash \npip install binary-cookies-parser\n```\nIf you want to use the parser as CLI, it\'s recommended to use pipx to install the package in an isolated environment.\n\n## Usage\nAfter installation, you can use the command-line interface to read a binary cookies file:\n\n```bash\nbcparser <path_to_binary_cookies_file>\n```\nReplace <path_to_binary_cookies_file> with the path to the binary cookie file you want to read.\n\nOr use it in Python:\n\n```python\nfrom binary_cookies_parser.parser import read_binary_cookies_file\n\ncookies = read_binary_cookies_file("path/to/cookies.binarycookies")\n```',
    'author': 'Daniel Tom',
    'author_email': 'daniel.tom@xebia.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
