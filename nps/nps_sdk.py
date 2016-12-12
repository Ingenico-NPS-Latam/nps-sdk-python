# -*- coding: utf-8 -*-
from nps.soapClient import SoapClient
from nps import services


class NpsSDK(SoapClient):

    def pay_online_2p(self, params):
        resp = self._soap_call(services.PAY_ONLINE_2P, params)
        return resp

    def authorize_2p(self, params):
        resp = self._soap_call(services.AUTHORIZE_2P, params)
        return resp

    def query_txs(self, params):
        resp = self._soap_call(services.QUERY_TXS, params)
        return resp

    def simple_query_tx(self, params):
        resp = self._soap_call(services.SIMPLE_QUERY_TX, params)
        return resp

    def refund(self, params):
        resp = self._soap_call(services.REFUND, params)
        return resp

    def capture(self, params):
        resp = self._soap_call(services.CAPTURE, params)
        return resp

    def authorize_3p(self, params):
        resp = self._soap_call(services.AUTHORIZE_3P, params)
        return resp

    def bank_payment_3p(self, params):
        resp = self._soap_call(services.BANK_PAYMENT_3P, params)
        return resp

    def cash_payment_3p(self, params):
        resp = self._soap_call(services.CASH_PAYMENT_3P, params)
        return resp

    def change_secret_key(self, params):
        resp = self._soap_call(services.CHANGE_SECRET_KEY, params)
        return resp

    def fraud_screening(self, params):
        resp = self._soap_call(services.FRAUD_SCREENING, params)
        return resp

    def notify_fraud_screening_review(self, params):
        resp = self._soap_call(services.NOTIFY_FRAUD_SCREENING_REVIEW, params)
        return resp

    def pay_online_3p(self, params):
        resp = self._soap_call(services.PAY_ONLINE_3P, params)
        return resp

    def split_authorize_3p(self, params):
        resp = self._soap_call(services.SPLIT_AUTHORIZE_3P, params)
        return resp

    def split_pay_online_3p(self, params):
        resp = self._soap_call(services.SPLIT_PAY_ONLINE_3P, params)
        return resp

    def query_card_number(self, params):
        resp = self._soap_call(services.QUERY_CARD_NUMBER, params)
        return resp

    def get_iin_details(self, params):
        resp = self._soap_call(services.GET_IIN_DETAILS, params)
        return resp


