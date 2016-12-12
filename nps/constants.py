import os
import sys

sdk = {'language': 'Python', 'version': '1.0'}
sys_ver = sys.version[0:7]
api = {'version': '2.2'}
PRODUCTION_ENV = 0
STAGING_ENV = 1
SANDBOX_ENV = 2
DEVELOPMENT_ENV = 3
dir = os.path.dirname(__file__)
wsdl_folder = "/wsdl/"
_FILE_SCHEMA = "file://"
_PRODUCTION_WSDL_NAME = "production.wsdl"
_SANDBOX_WSDL_NAME = "sandbox.wsdl"
_STAGING_WSDL_NAME = "staging.wsdl"
_DEVELOPMENT_WSDL_NAME = "development.wsdl"
_PRODUCTION_URL = _FILE_SCHEMA + dir + wsdl_folder + _PRODUCTION_WSDL_NAME
_SANDBOX_URL= _FILE_SCHEMA + dir + wsdl_folder + _SANDBOX_WSDL_NAME
_STAGING_URL = _FILE_SCHEMA + dir + wsdl_folder + _STAGING_WSDL_NAME
_DEVELOPMENT_URL = _FILE_SCHEMA + dir + wsdl_folder + _DEVELOPMENT_WSDL_NAME
DEF_TIMEOUT = 60