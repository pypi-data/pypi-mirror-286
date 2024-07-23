# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['churnzero_api_wrapper']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.32.3,<3.0.0']

setup_kwargs = {
    'name': 'churnzero-api-wrapper',
    'version': '0.2.0',
    'description': "A python package that wraps ChurnZero's HTTP API for easier usage of their HTTP API.",
    'long_description': '# ChurnZero Python API Wrapper\n\nThis is a Python API wrapper for the ChurnZero HTTP API. It provides a convenient way to interact with the ChurnZero HTTP API platform. The following features are supported:\n\n- Set Account Attributes (multi attributes only)\n- Set Contact Attributes (multi attributes only)\n- Track Events\n\nOther features may be supported in the future.\n\n> The wrapper only supports the HTTP API integrations documented on this page: [ChurnZero HTTP API](https://support.churnzero.com/hc/en-us/articles/360003183171-Integrate-ChurnZero-using-HTTP-API). REST features may be supported in the future.\n\n**Note**: This is an unofficial API wrapper and is not affiliated with ChurnZero.\n\n## Installation\n\nTo install the ChurnZero Python API Wrapper, you can use pip:\n\n```shell\npip install churnzero_api_wrapper\n```\n\n## Usage\n\nTo use the ChurnZero Python API Wrapper, you need to import the `ChurnZeroClient` class from the package:\n\n```python\nfrom churnzero_api_wrapper import HTTPClient\n```\n\nNext, you need to create an instance of the `HTTPClient` class and provide your ChurnZero APP credentials:\n\n```python\nclient = HTTPClient(app_key=\'{app_key}\', host = "https://{domain}.churnzero.net/i")\n```\n\nYour app key and domain can be found in the ChurnZero dashboard under `Admin` -> `Data` -> `Application Keys` -> `Application Key & HTTP API Endpoint`.\n\nOnce you have created the client, you can start making HTTP API requests. For example, to set an Account attribute:\n\n```python\naccount = {\n    "externalAccountID": "12345",\n    "attr{CustomAttribute1}": "Value1",\n}\nclient.set_account_attributes(account)\n```\n\nTo set a Contact attribute:\n\n```python\ncontact = {\n    "externalAccountID": "12345",\n    "externalContactID": "67890",\n    "attrFirstName": "Value1",\n    "attrLastName": "Value2",\n}\n\nclient.set_contact_attributes(contact)\n```\n\nTo track an event:\n\n```python\nevent = {\n    "externalAccountID": "12345",\n    "externalContactID": "67890",\n    "eventName": "EventName",\n    "description": "EventDescription",\n    "eventDate": "2021-01-01T00:00:00Z",\n}\n\nclient.track_event(event)\n```\n\n### Logging\n\nTo configure the logging level for the ChurnZero Python API Wrapper, you can use the `logging` module in Python. Here\'s an example of how to set the log level to `DEBUG`:\n\n```python\nimport logging\n\n# Set the log level to DEBUG\nlogging.getLogger().setLevel(logging.DEBUG)\n# Set the log level to INFO\nlogging.getLogger().setLevel(logging.INFO)\n# Set the log level to WARNING\nlogging.getLogger().setLevel(logging.WARNING)\n# Set the log level to ERROR\nlogging.getLogger().setLevel(logging.ERROR)\n```\n\n> <font color="red">**WARNING**</font>: note that setting the log level to `DEBUG` will expose the `app_key` to logs due to ChurnZero\'s HTTP API configuration. It is recommended to only use the `DEBUG` log level for debugging purposes and not in production environments.\n\n## Contributing\n\nContributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request on the GitHub repository.\n\n## License\n\nThis project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.\n',
    'author': 'Drew Ipson',
    'author_email': 'drewipson@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
