from distutils.core import setup
setup(
  name = 'nps',
  packages = ['nps'], # this must be the same as the name above
  version = '0.1.',
  description = 'A Python SDK for Ingenico ePayments - NPS LatAm Services',
  author = 'Gustavo Diaz',
  author_email = 'gustavo.diaz@ingenico.com',
  url = 'https://github.com/Ingenico-NPS-Latam/nps-sdk-python', # use the URL to the github repo
  download_url = 'https://github.com/Ingenico-NPS-Latam/nps-sdk-python/tarball/0.1', # I'll explain this in a second
  keywords = ['ingenico', 'payments', 'nps', 'nps-sdk'], # arbitrary keywords
  classifiers = [],
  install_requires=["suds-jurko=0.6"]
)