# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aws_jmespath_utils']

package_data = \
{'': ['*']}

install_requires = \
['jmespath>=1.0.1,<2.0.0']

setup_kwargs = {
    'name': 'aws-jmespath-utils',
    'version': '1.1.0',
    'description': 'jmespath custom functions for filtering and excluding AWS resources by tag',
    'long_description': '# aws-jmespath-utils\n\n## Installation\n\n```bash\npip3 install aws_jmespath_utils\n```\n\n## Examples\n\nCheck out the example code:\n\n- [examples/01_filter_tags_basic.py](./examples/01_filter_tags_basic.py)\n- [examples/02_filter_tags_exclude.py](./examples/02_filter_tags_exclude.py)\n\n## Usage\n\n**Find resources with \'Name\' tag set**\n\n```python\njmespath.search(  # it\'s important that your expression array must be inside `` backticks\n    \'[] | filter_tags(`["Name=*"]`, @)\', data_list, options=jmespath_options\n)\n```\n\n**Find tag values starting with 123**\n\n```python\njmespath.search(  # it\'s important that your expression array must be inside `` backticks\n    \'[].filter_tags(`["=123*"]`, @)\', data_list, options=jmespath_options\n)\n```\n\n**Find Many tag values**\n\n```python\njmespath.search(  # it\'s important that your expression array must be inside `` backticks\n    \'[].filter_tags(`["=123*", "=jmespath*"]`, @)\', data_list, options=jmespath_options\n)\n```\n\n**Exclude Tags**\n\n```python\njmespath.search(  # it\'s important that your expression array must be inside `` backticks\n    \'[].exclude_tags(`["map-migrated=*"]`, @)\', data_list, options=jmespath_options\n)\n```\n\n**Setting log levels**\n\n```bash\n# set log level as you wish\nexport AWS_JMESPATH_UTILS_LOG_LEVEL="DEBUG"   \nexport AWS_JMESPATH_UTILS_LOG_LEVEL="INFO"  # default   \n```\n\n\n\n## Complete Usage Example\n\n```python\nimport jmespath\nfrom aws_jmespath_utils import jmespath_options\nimport json\ndata_list = [    \n    {"a": "a", "Tags": [{"Key": "Name", "Value": "jmespath-utils"}, ]},\n    {"b": "b", "Tags": [{"Key": "Nam", "Value": "jmespath-utils-nam"}]},\n    {"c": "c", "Tags": [{"Key": "map-migrated", "Value": "234"}]}\n]\n\nprint(\n    json.dumps(\n        jmespath.search(\'[] | filter_tags(`["Name=*"]`, @)\', data_list, options=jmespath_options),\n        indent=2\n    )\n)\n\nprint(\n    json.dumps(\n        jmespath.search(\'[] | exclude_tags(`["Nam*="]`, @)\', data_list, options=jmespath_options),\n        indent=2\n    )\n)\n\n```',
    'author': 'Oguzhan Yilmaz',
    'author_email': 'oguzhanylmz271@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
