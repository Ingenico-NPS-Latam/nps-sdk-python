from nps.configuration import Configuration
from nps import utils
from requests.exceptions import ReadTimeout, ConnectTimeout
from nps.utils import RequestsTransport, LogPlugin, MaskedLogPlugin
from nps.errors import ApiException
from suds import client
import logging
from nps.file_adapter import FileAdapter
import requests
from suds.cache import NoCache
from requests.auth import HTTPProxyAuth


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
        elif Configuration.certificate:
            s.verify = Configuration.certificate

        t = RequestsTransport(s, timeout=Configuration.timeout)
        if Configuration.certificate is not None:
            self._client = client.Client(Configuration.get_wsdl().strip(), transport=t, plugins=plugings, cache=NoCache())
        else:
            self._client = client.Client(Configuration.get_wsdl().strip(), plugins=plugings, transport=t)

    def _soap_call(self, service, params):
        try:
            params = utils.add_extra_info(service, params)
            if Configuration.sanitize:
                params = utils._check_sanitize(params=params, is_root=True)

            params = utils.add_secure_hash(params)
            response = getattr(self._client.service, service)(params)
            return response
        except ReadTimeout:
            raise ApiException
        except ConnectTimeout:
            raise ApiException
