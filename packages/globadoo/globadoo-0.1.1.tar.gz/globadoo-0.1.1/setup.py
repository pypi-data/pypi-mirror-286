# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['globadoo']

package_data = \
{'': ['*']}

install_requires = \
['openai>=1.36.0,<2.0.0',
 'pydantic>=2.8.2,<3.0.0',
 'python-dotenv>=1.0.1,<2.0.0',
 'typer>=0.12.3,<0.13.0']

entry_points = \
{'console_scripts': ['globadoo = globadoo.main:main']}

setup_kwargs = {
    'name': 'globadoo',
    'version': '0.1.1',
    'description': "A CLI tool for finding countries based on city names using OpenAI's chat model",
    'long_description': '# Globadoo\n\nGlobadoo is a Python library for finding the country of a given city using OpenAI chat model.\n\n## Installation\n\nTo install Globadoo, use the following command:\n\n```\npip install globadoo\n```\n\n## Usage\n\nHere\'s a basic example of how to use Globadoo:\n\n```\npipx install globadoo\nexport OPENAI_API_KEY="your-api-key"\nglobadoo "New York"\n```\nThis returns\n    \n    {"city":"New York","country":"United States","country_code":"US"}\n\n## API Reference\n\nThe main function of Globadoo is `find_country(city, llm_config)`, which takes a city name and an LLMConfig model as arguments and returns the country of the city.\n\n## Tests\n\nTo run the tests for Globadoo, use the following command:\n\n```\npytest tests\n```\n\n## Contributing\n\nContributions to Globadoo are welcome. Please submit a pull request with your changes.\n\n## License\n\nGlobadoo is licensed under the MIT License.\n\n## Contact\n\nFor any questions or concerns, please open an issue on the GitHub repository.',
    'author': 'Daniel Tom',
    'author_email': 'd.e.tom89@gmail.com',
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
