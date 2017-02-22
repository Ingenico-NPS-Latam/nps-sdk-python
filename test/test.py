import unittest

class TestUtilsMethods(unittest.TestCase):

    def test_add_secure_hash(self):
        from nps_sdk.utils import add_secure_hash
        params = {'psp_QueryCriteriaId': '100409',
                  'psp_QueryCriteria': 'T',
                  'psp_Version': '2.2',
                  'psp_MerchantId': 'psp_test',
                  'psp_PosDateTime': '2016-12-01 12:00:00'}

        secret_key = "IeShlZMDk8mp8VA6vy41mLnVggnj1yqHcJyNqIYaRINZnXdiTfhF0Ule9WNAUCR6"

        resp = add_secure_hash(params, secret_key)
        self.assertEqual('d2f455e71232d7842c739196f6fa25f7', resp.get('psp_SecureHash'))
        self.assertEqual('psp_test', resp.get('psp_MerchantId'))
        self.assertEqual('100409', resp.get('psp_QueryCriteriaId'))


    def test_create_secure_hash(self):
        from nps_sdk.utils import _create_secure_hash
        secret_key = "IeShlZMDk8mp8VA6vy41mLnVggnj1yqHcJyNqIYaRINZnXdiTfhF0Ule9WNAUCR6"

        params = {'psp_QueryCriteriaId': '100409',
                  'psp_QueryCriteria': 'T',
                  'psp_Version': '2.2',
                  'psp_MerchantId': 'psp_test',
                  'psp_PosDateTime': '2016-12-01 12:00:00'}

        resp = _create_secure_hash(params, secret_key)
        self.assertEqual('d2f455e71232d7842c739196f6fa25f7', resp)

    def test_add_extra_info(self):
        from nps_sdk.utils import add_extra_info
        params = {'psp_QueryCriteriaId': '100409',
                  'psp_QueryCriteria': 'T',
                  'psp_Version': '2.2',
                  'psp_MerchantId': 'psp_test',
                  'psp_PosDateTime': '2016-12-01 12:00:00'}

        resp = add_extra_info('PayOnline_2p',params=params)
        self.assertTrue('psp_MerchantAdditionalDetails' in resp.keys())
        self.assertTrue('SdkInfo' in resp.get('psp_MerchantAdditionalDetails').keys())
        self.assertEqual('Python 1.0', resp.get('psp_MerchantAdditionalDetails').get('SdkInfo'))

    def _test_validate_size(self):
        from nps_sdk.utils import _validate_size
        from nps_sdk.conf.sanititize_struc import key_config
        value = 'Python 1.0'
        key = 'psp_MerchantAdditionalDetails.SdkInfo'
        resp = _validate_size(value=value, k=key)
        self.assertGreaterEqual(key_config.get(key+".max_length"), len(resp))

    def test_mask_credit_card(self):
        from nps_sdk.utils import _mask_c_number
        card_number = """<psp_CardNumber xsi:type="ns2:string">4507990000000011</psp_CardNumber>"""
        resp = _mask_c_number(card_number)
        self.assertEqual("""<psp_CardNumber xsi:type="ns2:string">450799******0011</psp_CardNumber>""", resp)

    def test_mask_cvc(self):
        from nps_sdk.utils import _mask_cvc
        cvc = """<psp_CardSecurityCode xsi:type="ns2:string">123</psp_CardSecurityCode>"""
        resp = _mask_cvc(cvc)
        self.assertEqual("""<psp_CardSecurityCode xsi:type="ns2:string">***</psp_CardSecurityCode>""", resp)

    def test_mask_exp_date(self):
        from nps_sdk.utils import _mask_exp_date
        card_exp_date = """<psp_CardExpDate xsi:type="ns2:string">1712</psp_CardExpDate>"""
        resp = _mask_exp_date(card_exp_date)
        self.assertEqual("""<psp_CardExpDate xsi:type="ns2:string">****</psp_CardExpDate>""", resp)


    def test_mask_data(self):
        from nps_sdk.utils import _mask_data
        datos = """
        <psp_CardExpDate xsi:type="ns2:string">1712</psp_CardExpDate>
        <psp_CardSecurityCode xsi:type="ns2:string">123</psp_CardSecurityCode>
        <psp_CardNumber xsi:type="ns2:string">4507990000000011</psp_CardNumber>
        """
        espected = """
        <psp_CardExpDate xsi:type="ns2:string">****</psp_CardExpDate>
        <psp_CardSecurityCode xsi:type="ns2:string">***</psp_CardSecurityCode>
        <psp_CardNumber xsi:type="ns2:string">450799******0011</psp_CardNumber>
        """
        resp = _mask_data(datos)
        self.assertEqual(espected, resp)

    def test_find_c_numbers(self):
        from nps_sdk.utils import _find_c_numbers
        datos = """
                <psp_CardExpDate xsi:type="ns2:string">1712</psp_CardExpDate>
                <psp_CardSecurityCode xsi:type="ns2:string">123</psp_CardSecurityCode>
                <psp_CardNumber xsi:type="ns2:string">4507990000000011</psp_CardNumber>
                """

        resp = _find_c_numbers(datos)
        self.assertEqual(['4507990000000011</psp_CardNumber>'], resp)

    def test_find_exp_date(self):
        from nps_sdk.utils import _find_exp_date
        datos = """
                <psp_CardExpDate xsi:type="ns2:string">1712</psp_CardExpDate>
                <psp_CardSecurityCode xsi:type="ns2:string">123</psp_CardSecurityCode>
                <psp_CardNumber xsi:type="ns2:string">4507990000000011</psp_CardNumber>
                """
        resp = _find_exp_date(datos)
        self.assertEqual(['1712</psp_CardExpDate>'], resp)

    def test_find_cvc(self):
        from nps_sdk.utils import _find_cvc
        datos = """
                <psp_CardExpDate xsi:type="ns2:string">1712</psp_CardExpDate>
                <psp_CardSecurityCode xsi:type="ns2:string">123</psp_CardSecurityCode>
                <psp_CardNumber xsi:type="ns2:string">4507990000000011</psp_CardNumber>
                """
        resp = _find_cvc(datos)
        self.assertEqual(['123</psp_CardSecurityCode>'], resp)


class TestServices(unittest.TestCase):

    def test_get_not_add_services(self):
        from nps_sdk.services import get_merch_det_not_add_services
        espected = ['QueryTxs', 'Refund', 'SimpleQueryTx', 'Capture', 'ChangeSecretKey', 'NotifyFraudScreeningReview', 'GetIINDetails', 'QueryCardNumber', 'CreatePaymentMethod', 'CreatePaymentMethodFromPayment', 'RetrievePaymentMethod', 'UpdatePaymentMethod', 'DeletePaymentMethod', 'CreateCustomer', 'RetrieveCustomer', 'UpdateCustomer', 'DeleteCustomer', 'RecachePaymentMethodToken', 'CreatePaymentMethodToken', 'RetrievePaymentMethodToken', 'CreateClientSession', 'GetInstallmentsOptions', 'QueryCardDetails']
        resp = get_merch_det_not_add_services()
        self.assertEqual(espected, resp)