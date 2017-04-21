import collections
import hashlib
import requests
import suds.transport as transport
from nps_sdk import services
from nps_sdk.constants import sdk
from nps_sdk import Configuration
from nps_sdk.conf import sanititize_struc
from suds.plugin import MessagePlugin
import logging
import re

_log_format = '%(asctime)s - NpsSDK - %(levelname)s - %(message)s'

class Enum(set):
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError

try:
    from StringIO import StringIO as ios
except ImportError:
    from io import BytesIO as ios

__all__ = ['RequestsTransport']


class RequestsTransport(transport.Transport):
    def __init__(self, session=None, **kwargs):
        transport.Transport.__init__(self)
        self._session = session or requests.Session()
        self._kwargs = kwargs

    def open(self, request):
        resp = self._session.get(request.url, timeout=self._kwargs.get('timeout', 60))
        resp.raise_for_status()
        return ios(resp.content)

    def send(self, request):
        resp = self._session.post(
            request.url,
            data=request.message,
            headers=request.headers,
            json=None, timeout=self._kwargs.get('timeout', 60))

        if resp.headers.get('content-type') not in ('text/xml',
                                                    'application/soap+xml'):
            resp.raise_for_status()
        return transport.Reply(
            resp.status_code,
            resp.headers,
            resp.content,
        )

def add_extra_info(service, params):
    if service in services.get_merch_det_not_add_services():
        return params
    info = {"SdkInfo": sdk.get('language') + ' ' + sdk.get('version')}
    params.update({"psp_MerchantAdditionalDetails": info})
    return params

def add_secure_hash(params, secret_key):
    secure_hash = _create_secure_hash(params, secret_key)
    params.update({"psp_SecureHash": secure_hash})
    return params


def _create_secure_hash(params, secret_key):
    m = hashlib.md5()
    od = collections.OrderedDict(sorted(params.items()))
    concatenated_data = "".join([str(x).strip() for x in od.values() if type(x) is not dict and type(x) is not list]) + secret_key
    concatenated_data = concatenated_data.encode('utf-8')
    m.update(concatenated_data)
    coded = m.hexdigest()
    return coded


def _check_sanitize(params, is_root=False, nodo = None):
    if is_root:
        result_params = {}
    else:
        result_params = params
    for k, v in params.items():
        if type(v) is dict:
            result_params.update({k: _check_sanitize(v, nodo=k)})
        elif type(v) is list:
            result_params.update({k: check_sanitize_array(v, nodo=k)})
        else:
            result_params.update({k: _validate_size(v, k, nodo)})

    return result_params


def check_sanitize_array(params, nodo):
    result_params = []
    for x in params:
        result_params.append(_check_sanitize(x, nodo=nodo))
    return result_params


def _validate_size(value, k=None, nodo=None):
    if nodo is not None:
        key_name = nodo + "." + k + ".max_length"
    else:
        key_name = k + ".max_length"
    size = sanititize_struc.key_config.get(key_name)
    return str(value)[0:size]


def _mask_data(data):
    data = data.decode('utf-8')
    data = _mask_c_number(data)
    data = _mask_exp_date(data)
    data = _mask_cvc(data)
    data = _mask_tokenization_c_number(data)
    data = _mask_tokenization_exp_date(data)
    data = _mask_tokenization_cvc(data)

    return data


def _mask_c_number(data):
    c_number_key = "</psp_CardNumber>"
    c_numbers = _find_c_numbers(data, c_number_key)
    for c_number in c_numbers:
        c_number_len = len(c_number[0: len(c_number) - len(c_number_key)])
        masked_chars = c_number_len - 10
        data = data.replace(c_number,
                            c_number[0: 6] + "*"*masked_chars + c_number[len(c_number)-4-len(c_number_key): len(c_number)])

    return data

def _mask_exp_date(data):
    exp_date_key = "</psp_CardExpDate>"
    exp_dates = _find_exp_date(data, exp_date_key)
    for exp_date in exp_dates:
        data = data.replace(exp_date, "****" + exp_date_key)
    return data

def _mask_cvc(data):
    cvc_key = "</psp_CardSecurityCode>"
    cvcs = _find_cvc(data, cvc_key)
    for cvc in cvcs:
        cvc_len = len(cvc[0: len(cvc) - len(cvc_key)])
        data = data.replace(cvc, "*"*cvc_len + cvc_key)
    return data

def _mask_tokenization_c_number(data):
    c_number_key = "</Number>"
    c_numbers = _find_c_numbers(data, c_number_key)
    for c_number in c_numbers:
        c_number_len = len(c_number[0: len(c_number) - len(c_number_key)])
        masked_chars = c_number_len - 10
        data = data.replace(c_number,
                            c_number[0: 6] + "*"*masked_chars + c_number[len(c_number)-4-len(c_number_key): len(c_number)])

    return data

def _mask_tokenization_exp_date(data):
    exp_date_key = "</ExpirationDate>"
    exp_dates = _find_exp_date(data, exp_date_key)
    for exp_date in exp_dates:
        data = data.replace(exp_date, "****" + exp_date_key)
    return data

def _mask_tokenization_cvc(data):
    cvc_key = "</SecurityCode>"
    cvcs = _find_cvc(data, cvc_key)
    for cvc in cvcs:
        cvc_len = len(cvc[0: len(cvc) - len(cvc_key)])
        data = data.replace(cvc, "*"*cvc_len + cvc_key)
    return data


def _find_c_numbers(data, key):
    c_numbers = re.findall("\d{13,19}" + key, data)
    return c_numbers


def _find_exp_date(data, key):
    exp_dates = re.findall("\d{4}" + key, data)
    return exp_dates


def _find_cvc(data, key):
    cvcs = re.findall("\d{3,4}" + key, data)
    return cvcs


def _parse_to_xml(text):
    import xml.dom.minidom
    xml = xml.dom.minidom.parseString(text)
    pretty_xml_as_string = xml.toprettyxml()
    return pretty_xml_as_string

def get_log_format():
    return _log_format


class LogPlugin(MessagePlugin):

    def sending(self, context):
        logging.info(_parse_to_xml(context.envelope))

    def received(self, context):
        logging.info(_parse_to_xml(context.reply))


class MaskedLogPlugin(MessagePlugin):

    def sending(self, context):
        logging.info(_parse_to_xml(_mask_data(context.envelope)))

    def received(self, context):
        logging.info(_parse_to_xml(_mask_data(context.reply)))


class OutgoingFilter(logging.Filter):
    def filter(self, record):
        return record.msg.startswith('sending:')





