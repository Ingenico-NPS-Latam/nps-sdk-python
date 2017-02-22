PAY_ONLINE_2P = "PayOnLine_2p"
AUTHORIZE_2P = "Authorize_2p"
QUERY_TXS = "QueryTxs"
SIMPLE_QUERY_TX = "SimpleQueryTx"
REFUND = "Refund"
CAPTURE = "Capture"
AUTHORIZE_3P = "Authorize_3p"
BANK_PAYMENT_3P = "BankPayment_3p"
CASH_PAYMENT_3P = "CashPayment_3p"
CHANGE_SECRET_KEY = "ChangeSecretKey"
FRAUD_SCREENING = "FraudScreening"
NOTIFY_FRAUD_SCREENING_REVIEW = "NotifyFraudScreeningReview"
PAY_ONLINE_3P = "PayOnLine_3p"
SPLIT_AUTHORIZE_3P = "SplitAuthorize_3p"
SPLIT_PAY_ONLINE_3P = "SplitPayOnLine_3p"
BANK_PAYMENT_2P = "BankPayment_2p"
SPLIT_PAY_ONLINE_2P = "SplitPayOnLine_2p"
SPLIT_AUTHORIZE_2P = "SplitAuthorize_2p"
QUERY_CARD_NUMBER = "QueryCardNumber"
QUERY_CARD_DETAILS = "QueryCardDetails"
GET_IIN_DETAILS = "GetIINDetails"

CREATE_PAYMENT_METHOD = "CreatePaymentMethod"
CREATE_PAYMENT_METHOD_FROM_PAYMENT = "CreatePaymentMethodFromPayment"
RETRIEVE_PAYMENT_METHOD = "RetrievePaymentMethod"
UPDATE_PAYMENT_METHOD = "UpdatePaymentMethod"
DELETE_PAYMENT_METHOD = "DeletePaymentMethod"
CREATE_CUSTOMER = "CreateCustomer"
RETRIEVE_CUSTOMER = "RetrieveCustomer"
UPDATE_CUSTOMER = "UpdateCustomer"
DELETE_CUSTOMER = "DeleteCustomer"
RECACHE_PAYMENT_METHOD_TOKEN = "RecachePaymentMethodToken"
CREATE_PAYMENT_METHOD_TOKEN = "CreatePaymentMethodToken"
RETRIEVE_PAYMENT_METHOD_TOKEN = "RetrievePaymentMethodToken"
CREATE_CLIENT_SESSION = "CreateClientSession"
GET_INSTALLMENTS_OPTIONS = "GetInstallmentsOptions"


def get_merch_det_not_add_services():
    return [QUERY_TXS,
            REFUND,
            SIMPLE_QUERY_TX,
            CAPTURE,
            CHANGE_SECRET_KEY,
            NOTIFY_FRAUD_SCREENING_REVIEW,
            GET_IIN_DETAILS,
            QUERY_CARD_NUMBER,
            CREATE_PAYMENT_METHOD,
            CREATE_PAYMENT_METHOD_FROM_PAYMENT,
            RETRIEVE_PAYMENT_METHOD,
            UPDATE_PAYMENT_METHOD,
            DELETE_PAYMENT_METHOD,
            CREATE_CUSTOMER,
            RETRIEVE_CUSTOMER,
            UPDATE_CUSTOMER,
            DELETE_CUSTOMER,
            RECACHE_PAYMENT_METHOD_TOKEN,
            CREATE_PAYMENT_METHOD_TOKEN,
            RETRIEVE_PAYMENT_METHOD_TOKEN,
            CREATE_CLIENT_SESSION,
            GET_INSTALLMENTS_OPTIONS,
            QUERY_CARD_DETAILS]
