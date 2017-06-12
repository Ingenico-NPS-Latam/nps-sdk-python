version = '1.1.11'

from setuptools import setup, find_packages

setup(
  name = 'nps_sdk',
  packages = find_packages(),
  version = version,
  description = 'A Python SDK for Ingenico ePayments - NPS LatAm Services',
  author = 'Gustavo Diaz',
  author_email = 'gustavo.diaz@ingenico.com',
  url = 'https://github.com/Ingenico-NPS-Latam/nps-sdk-python',
  keywords = ['ingenico', 'payments', 'npssdk', 'nps-sdk'],
  classifiers = [
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules"],
  install_requires=['suds-jurko==0.6', 'requests==2.9.1', 'six==1.10.0'],
  package_data={ 'nps_sdk': ['wsdl/staging.wsdl',
                         'wsdl/sandbox.wsdl',
                         'wsdl/production.wsdl',
                         'wsdl/development.wsdl'] }
)