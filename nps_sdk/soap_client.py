from nps_sdk.configuration import Configuration
from nps_sdk import utils, constants
from requests.exceptions import ReadTimeout, ConnectTimeout
from nps_sdk.utils import RequestsTransport, LogPlugin, MaskedLogPlugin
from nps_sdk.errors import ApiException, LogException
from suds import client
import logging
from nps_sdk.file_adapter import FileAdapter
import requests
from suds.cache import NoCache
from requests.auth import HTTPProxyAuth
import requests

class SoapClient(object):
    def __init__(self):
        self._setup()

    def _setup(self):
        plugings = []
        if Configuration.debug:
            if Configuration.log_file is not None:
                logging.basicConfig(filename=Configuration.log_file, level=Configuration.log_level,
                                    format=utils.get_log_format())
            else:
                logging.basicConfig(level=Configuration.log_level,
                                    format=utils.get_log_format())

            if Configuration.log_level == logging.DEBUG and Configuration.environment ==  constants.PRODUCTION_ENV:
                raise LogException

            if Configuration.log_level > logging.DEBUG or Configuration.log_level == 0:
                plugings.append(MaskedLogPlugin())
            else:
                plugings.append(LogPlugin())


        s = requests.Session()
        s.mount('file://', FileAdapter())
        if Configuration.proxy_url:
            s.proxies = { 'https': Configuration.proxy_url }
            if Configuration.proxy_username:
                s.auth= HTTPProxyAuth(Configuration.proxy_username, Configuration.proxy_password)

        if Configuration.certificate and Configuration.c_key:
            s.cert=(Configuration.certificate, Configuration.c_key)
        else:
            if not Configuration.certificate:
                pass
                #from requests.packages.urllib3.exceptions import InsecureRequestWarning
                #requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

            s.verify = Configuration.certificate

        t = RequestsTransport(s, timeout=Configuration.timeout)
        self._client = client.Client(Configuration.get_wsdl().strip(), plugins=plugings, transport=t, cache=NoCache())

    def _soap_call(self, service, params):
        try:
            params = utils.add_extra_info(service, params)
            if Configuration.sanitize:
                params = utils._check_sanitize(params=params, is_root=True)
            if not params.get('psp_ClientSession'):
                params = utils.add_secure_hash(params, Configuration.secret_key)

            response = getattr(self._client.service, service)(params)
            return response
        except ReadTimeout:
            raise ApiException
        except ConnectTimeout:
            raise ApiException
