# -*- coding: utf-8 -*-
import sys
try:
    reload(sys)
    sys.setdefaultencoding('utf8')
except NameError:
    pass


class TransactionException(Exception):
    msg = """
            Response code: %s
            Response Message: %s
            Extended Response Message: %s
            """

    def __init__(self, response):
        self._resp_code = response.psp_ResponseCod.encode('utf-8')
        self._resp_msg = response.psp_ResponseMsg.encode('utf-8')
        self._resp_msg_ext = response.psp_ResponseExtended.encode('utf-8')
        self._response = response
        Exception.__init__(self,
                           TransactionException.msg % (self._resp_code,
                                                       self._resp_msg,
                                                       self._resp_msg_ext))

    def get_message(self):
        return self._response.psp_ResponseMsg

    def get_extended_message(self):
        return self._response.psp_ResponseExtended

    def get_raw_response(self):
        return self._response


class RejectedException(TransactionException):
    pass


class DeclinedException(TransactionException):
    pass


class MethodNotFoundException(Exception):
    msg = """El metodo %s no fué encontrado"""

    def __init__(self, name):
        Exception.__init__(self, MethodNotFoundException.msg % (name))


class ApiException(Exception):
    msg = """
            El tiempo de ejecución há expirado
            """

    def __init__(self):
        Exception.__init__(self, ApiException.msg)


class LogException(Exception):
    msg = """
            DEBUG level is now allowed in PRODUCTION ENVIRONMENT
            """

    def __init__(self):
        Exception.__init__(self, LogException.msg)


class EnvironmentNotFound(Exception):
    msg = """
            El ambiente seleccionado es invalido.
            los ambientes validos son
            0: PRODUCCION
            1: STAGING
            2: SANDBOX
            """

    def __init__(self):
        Exception.__init__(self, EnvironmentNotFound.msg)