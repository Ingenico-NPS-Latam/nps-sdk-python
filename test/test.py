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

class TestIssues(unittest.TestCase):

    def test_secure_hash_w_list_in_root_node(self):
        from nps_sdk.utils import _create_secure_hash

        key = "IeShlZMDk8mp8VA6vy41mLnVggnj1yqHcJyNqIYaRINZnXdiTfhF0Ule9WNAUCR6"

        params = {
            "psp_Version": '2.2',
            "psp_MerchantId": 'psp_test',
            "psp_TxSource": 'WEB',
            "psp_MerchOrderId": 'ORDER999qdw',
            "psp_ReturnURL": 'http://localhost/',
            "psp_FrmLanguage": 'es_AR',
            "psp_Amount": 15050,
            "psp_Currency": '032',
            "psp_Country": 'ARG',
            "psp_Product": 14,
            "psp_PosDateTime": '2016-12-01 12:00:00',
            "psp_Transactions": [{
                "psp_MerchantId": 'psp_test',
                "psp_MerchTxRef": 'ORDER36qx6-3',
                "psp_Product": 14,
                "psp_Amount": 10000,
                "psp_NumPayments": 1
            },{
                "psp_MerchantId": 'psp_test',
                "psp_MerchTxRef": 'ORDER1qd66-3',
                "psp_Product": 14,
                "psp_Amount": 5050,
                "psp_NumPayments": 1
            }]
        }

        resp = _create_secure_hash(params=params, secret_key=key)
        self.assertEqual("a4defbaaaf41d581c8a35014820404df", resp)


    def test_issue_3930_error_500_on_p2p_with_updated_costumer_on_dev(self):
        from nps_sdk.constants import DEVELOPMENT_ENV, SANDBOX_ENV
        import nps_sdk
        import logging
        import uuid
        merch_ref = uuid.uuid4()

        nps_sdk.Configuration.configure(environment=SANDBOX_ENV,
                                        secret_key="IeShlZMDk8mp8VA6vy41mLnVggnj1yqHcJyNqIYaRINZnXdiTfhF0Ule9WNAUCR6",
                                        log_level=logging.INFO, debug=True, cert_verify_peer=False)

        sdk = nps_sdk.Nps()

        merchant_id = 'psp_test'

        params = {'psp_AccountCreatedAt': '2010-10-23',
                  'psp_EmailAddress': 'fedevalle@inclufin.com',
                  'psp_MerchantId': merchant_id,
                  'psp_Person': {'FirstName': 'Federico',
                                 'LastName': 'del Valle',
                                 'PhoneNumber1': '+5491164838755'},
                  'psp_PosDateTime': '2017-02-09 18:42:43',
                  'psp_Version': '2.2'}

        create_customer_response = sdk.create_customer(params)


        params = {
            'psp_AccountCreatedAt': '2010-10-23',
            'psp_Address': {
                'AdditionalInfo': '2 A',
                'City': 'Miami',
                'Country': 'USA',
                'HouseNumber': '1245',
                'StateProvince': 'Florida',
                'Street': 'Av. Collins',
                'ZipCode': '33140'
            },
            'psp_AlternativeEmailAddress': 'jdoe@example.com',
            'psp_CustomerId': create_customer_response.psp_CustomerId,
            'psp_EmailAddress': 'jhon.doe@example.com',
            'psp_MerchantId': merchant_id,
            'psp_PaymentMethod': {
                'CardInputDetails': {
                    'ExpirationDate': '1909',
                    'HolderName': 'VISA',
                    'Number': '4242424242424242',
                    'SecurityCode': '9822'
                },
                'Product': '14'
            },
            'psp_Person': {
                'DateOfBirth': '1979-01-12',
                'FirstName': 'John',
                'Gender': 'M',
                'IDNumber': '54111111',
                'IDType': '200',
                'LastName': 'Doe',
                'MiddleName': 'Michael',
                'Nationality': 'ARG',
                'PhoneNumber1': '+1 011 11111111',
                'PhoneNumber2': '+1 011 22222222'
            },
            'psp_PosDateTime': '2008-01-12 13:05:00',
            'psp_Version': '2.2'
        }

        update_customer_response = sdk.update_customer(params)

        params = {
            'psp_MerchOrderId': merch_ref,
            'psp_VaultReference': {
                'CustomerId': update_customer_response.psp_CustomerId
            },
            'psp_MerchTxRef': merch_ref,
            'psp_PosDateTime': '2017-03-31 16:14:06',
            'psp_NumPayments': '1',
            'psp_Currency': '032',
            'psp_TxSource': 'WEB',
            'psp_Product': '14',
            'psp_Country': 'ARG',
            'psp_Version': '2.2',
            'psp_MerchantId': merchant_id,
            'psp_Amount': "1000"
        }

        p2p_response = sdk.pay_online_2p(params)


        self.assertEqual("2", p2p_response.psp_ResponseCod)


    def test_response_of_p2p_with_billing_details(self):
        from nps_sdk.constants import DEVELOPMENT_ENV, SANDBOX_ENV
        import nps_sdk
        import logging
        import uuid
        merch_ref = uuid.uuid4()

        nps_sdk.Configuration.configure(environment=SANDBOX_ENV,
                                        secret_key="IeShlZMDk8mp8VA6vy41mLnVggnj1yqHcJyNqIYaRINZnXdiTfhF0Ule9WNAUCR6",
                                        log_level=logging.INFO, debug=True, cert_verify_peer=False)

        sdk = nps_sdk.Nps()

        merchant_id = 'psp_test'

        params = {
                    "psp_Version": '2.2',
                    "psp_MerchantId": merchant_id,
                    "psp_TxSource": 'WEB',
                    "psp_MerchTxRef": merch_ref,
                    "psp_MerchOrderId": merch_ref,
                    "psp_Amount": '15050',
                    "psp_NumPayments": '1',
                    "psp_Currency": '032',
                    "psp_Country": 'ARG',
                    "psp_Product": '14',
                    "psp_CardNumber": '4850110000000000',
                    "psp_CardExpDate": '1712',
                    "psp_PosDateTime": '2016-12-01 12:00:00',
                    "psp_CardSecurityCode": '123',
                    "psp_CardHolderName": "Gustavo Diaz",
                    "psp_PurchaseDescription" : "Juguetes",
                    "psp_BillingDetails": {
                        "Invoice": "123",
                        "Invoice": "2017-01-01",
                        "InvoiceAmount": "123",
                        "InvoiceCurrency": "032",
                        "Person": {
                            'FirstName': 'John',
                            'LastName': 'Doe',
                            'MiddleName': 'Michael',
                            'PhoneNumber1': '+1 011 11111111',
                            'PhoneNumber2': '+1 011 22222222',
                            'DateOfBirth': '1979-01-12',
                            'Gender': 'M',
                            'Nationality': 'ARG',
                            'IDNumber': '54111111',
                            'IDType': '200'
                        },
                        'Address': {
                            'Street': 'Av. Collins',
                            'HouseNumber': '1245',
                            'AdditionalInfo': '2 A',
                            'StateProvince': 'Florida',
                            'City': 'Miami',
                            'Country': 'USA',
                            'ZipCode': '33140'
                        }
                    }
                  }

        resp = sdk.pay_online_2p(params)

        params = {
            "psp_Version": '2.2',
            "psp_MerchantId": merchant_id,
            "psp_QueryCriteria": 'T',
            "psp_QueryCriteriaId": resp.psp_TransactionId,
            "psp_PosDateTime": '2016-12-01 12:00:00'
        }

        resp = sdk.simple_query_tx(params)
        print resp


    def test_add_two_payment_methods_to_client(self):
        from nps_sdk.constants import DEVELOPMENT_ENV, SANDBOX_ENV
        import nps_sdk
        import logging
        import uuid
        merch_ref = uuid.uuid4()

        nps_sdk.Configuration.configure(environment=SANDBOX_ENV,
                                        #secret_key="IeShlZMDk8mp8VA6vy41mLnVggnj1yqHcJyNqIYaRINZnXdiTfhF0Ule9WNAUCR6",
                                        secret_key="swGYxNeehNO8fS1zgwvCICevqjHbXcwPWAvTVZ5CuULZwKWaGPmXbPSP8i1fKv2q",
                                        log_level=logging.INFO, debug=True, cert_verify_peer=False)
        sdk = nps_sdk.Nps()
        merchant_id = 'sdk_test'

        params = {
            'psp_Version': '2.2',
            'psp_MerchantId': merchant_id,
            'psp_PosDateTime': '2017-01-01 12:00:00'
        }
        resp = sdk.create_client_session(params)

        params = {'psp_Address': {'AdditionalInfo': '2 A',
                                  'City': 'Miami',
                                  'Country': 'USA',
                                  'HouseNumber': '1245',
                                  'StateProvince': 'Florida',
                                  'Street': 'Av. Collins',
                                  'ZipCode': '33140'},
                  'psp_CardInputDetails': {'ExpirationDate': '1909',
                                           'HolderName': 'sol',
                                           'Number': '4242424242424243',
                                           'SecurityCode': '123'},
                  'psp_ClientSession': resp.psp_ClientSession,
                  'psp_MerchantId': merchant_id,
                  'psp_Person': {'DateOfBirth': '1979-01-12',
                                 'FirstName': 'John',
                                 'Gender': 'M',
                                 'IDNumber': '54111111',
                                 'IDType': '200',
                                 'LastName': 'Doe',
                                 'MiddleName': 'Michael',
                                 'Nationality': 'ARG',
                                 'PhoneNumber1': '+1 011 11111111',
                                 'PhoneNumber2': '+1 011 22222222'},
                  'psp_Product': '14',
                  'psp_Version': '2.2'}

        resp_cppt = sdk.create_payment_method_token(params)

        params = {
            'psp_Version': '2.2',
            'psp_MerchantId': merchant_id,
            'psp_EmailAddress': 'jhon.doe@example.com',
            'psp_AlternativeEmailAddress': 'jdoe@example.com',
            'psp_AccountID': 'jdoe78',
            'psp_AccountCreatedAt': '2010-10-23',
            'psp_PosDateTime': '2008-01-12 13:05:00',
            'psp_Person': {
                'FirstName': 'John',
                'LastName': 'Doe',
                'MiddleName': 'Michael',
                'PhoneNumber1': '+1 011 11111111',
                'PhoneNumber2': '+1 011 22222222',
                'DateOfBirth': '1979-01-12',
                'Gender': 'M',
                'Nationality': 'ARG',
                'IDNumber': '54111111',
                'IDType': '200'
            },
            'psp_Address': {
                'Street': 'Av. Collins',
                'HouseNumber': '1245',
                'AdditionalInfo': '2 A',
                'StateProvince': 'Florida',
                'City': 'Miami',
                'Country': 'USA',
                'ZipCode': '33140'
            }
        }

        resp_cc = sdk.create_customer(params)

        params = {
                    'psp_MerchantId': merchant_id,
                    'psp_CustomerId': resp_cc.psp_CustomerId,
                    'psp_PaymentMethod': {
                        'PaymentMethodToken': resp_cppt.psp_PaymentMethodToken
                    },
                    'psp_PosDateTime': '2008-01-12 13:05:00',
                    'psp_SetAsCustomerDefault': '1',
                    'psp_Version': '2.2'
                }

        resp_cpm1 = sdk.create_payment_method(params)
        resp_cpm1 = sdk.create_payment_method(params)

        params = {
            'psp_CustomerId': resp_cc.psp_CustomerId,
            'psp_MerchantId': merchant_id,
            'psp_PosDateTime': '2008-01-12 13:05:00',
            'psp_Version': '2.2'
        }

        resp = sdk.retrieve_customer(params)


    def test_get_customer(test):
        from nps_sdk.constants import DEVELOPMENT_ENV, SANDBOX_ENV
        import nps_sdk
        import logging
        import uuid
        merch_ref = uuid.uuid4()

        nps_sdk.Configuration.configure(environment=SANDBOX_ENV,
                                        secret_key="IeShlZMDk8mp8VA6vy41mLnVggnj1yqHcJyNqIYaRINZnXdiTfhF0Ule9WNAUCR6",
                                        #secret_key="swGYxNeehNO8fS1zgwvCICevqjHbXcwPWAvTVZ5CuULZwKWaGPmXbPSP8i1fKv2q",
                                        log_level=logging.INFO, debug=True, cert_verify_peer=False)
        sdk = nps_sdk.Nps()
        merchant_id = 'psp_test'

        params = {
            'psp_CustomerId': '5hnNzGs2lMPw2ch33Yi0Ep334dDIoStQ',
            'psp_MerchantId': merchant_id,
            'psp_PosDateTime': '2008-01-12 13:05:00',
            'psp_Version': '2.2'
        }

        resp = sdk.retrieve_customer(params)
