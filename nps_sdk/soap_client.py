from nps_sdk.configuration import Configuration
from nps_sdk import utils, constants
from requests.exceptions import ReadTimeout, ConnectTimeout
from nps_sdk.utils import RequestsTransport, LogPlugin
from nps_sdk.errors import ApiException, LogException
from suds import client
import logging
from nps_sdk.file_adapter import FileAdapter
from suds.cache import NoCache, FileCache, DocumentCache, ObjectCache
from requests.auth import HTTPProxyAuth
import requests

class SoapClient(object):
    def __init__(self):
        self._setup()

    def _setup(self):
        plugings = []
        cache_conf = NoCache()
        if Configuration.debug:
            if Configuration.log_file is not None:
                logging.basicConfig(filename=Configuration.log_file, level=Configuration.log_level,
                                    format=utils.get_log_format())
            else:
                logging.basicConfig(level=Configuration.log_level,
                                    format=utils.get_log_format())

            if Configuration.log_level == logging.DEBUG and Configuration.environment ==  constants.PRODUCTION_ENV:
                raise LogException

            plugings.append(LogPlugin())


        s = requests.Session()
        s.mount('file://', FileAdapter())
        if Configuration.proxy_url:
            s.proxies = utils.get_builded_proxy_url(Configuration.proxy_url, Configuration.proxy_port)
            if Configuration.proxy_user:
                s.auth= HTTPProxyAuth(Configuration.proxy_user, Configuration.proxy_pass)

        if Configuration.certificate and Configuration.c_key:
            s.cert=(Configuration.certificate, Configuration.c_key)
        else:
            s.verify = Configuration.certificate

        t = RequestsTransport(s, timeout=Configuration.timeout)

        if Configuration.cache:
            cache_conf = ObjectCache(location=Configuration.cache_location, seconds=Configuration.cache_duration)

        self._client = client.Client(Configuration.get_wsdl().strip(), plugins=plugings, transport=t, cache=cache_conf)

    def _soap_call(self, service, params):
        try:
            params = utils.add_extra_info(service, params)
            if Configuration.sanitize:
                params = utils._check_sanitize(params=params, is_root=True)
            if not params.get('psp_ClientSession'):
                params = utils.add_secure_hash(params, Configuration.secret_key)
            response = getattr(self._client.service, service)(params)
            if not Configuration.as_obj:
                response = utils.recursive_asdict(response)
            return response
        except ReadTimeout as e:
            logging.warning(e.message)
            raise ApiException
        except ConnectTimeout as e:
            logging.warning(e.message)
            raise ApiException
