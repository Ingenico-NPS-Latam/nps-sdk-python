from nps_sdk import constants
from nps_sdk import errors
import logging


class Configuration(object):

    @staticmethod
    def configure(environment=constants.SANDBOX_ENV,
                  secret_key="",
                  debug=False,
                  timeout=60,
                  cert_verify_peer=True,
                  log_level=logging.INFO,
                  **kwargs):
        Configuration.environment = environment
        Configuration.secret_key = secret_key
        Configuration.debug = debug
        Configuration.timeout = timeout
        Configuration.cert_verify_peer = True
        Configuration.log_level = log_level
        Configuration.certificate = kwargs.get('cert', cert_verify_peer)
        Configuration.c_key = kwargs.get('key_cert')
        Configuration.sanitize = kwargs.get('sanitize', True)
        Configuration.log_file = kwargs.get('log_file')
        Configuration.proxy_url = kwargs.get('proxy_url')
        Configuration.proxy_username = kwargs.get('proxy_username')
        Configuration.proxy_password = kwargs.get('proxy_password')

    @staticmethod
    def get_wsdl():
        try:
            if Configuration.environment < 0:
                raise IndexError
            envs = (constants._PRODUCTION_URL,
                    constants._STAGING_URL,
                    constants._SANDBOX_URL,
                    constants._DEVELOPMENT_URL)
            return envs[Configuration.environment]
        except IndexError:
            raise errors.EnvironmentNotFound

