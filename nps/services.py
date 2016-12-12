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
GET_IIN_DETAILS = "GetIINDetails"


def get_merch_det_not_add_services():
    return [QUERY_TXS,
            REFUND,
            SIMPLE_QUERY_TX,
            CAPTURE,
            CHANGE_SECRET_KEY,
            NOTIFY_FRAUD_SCREENING_REVIEW,
            GET_IIN_DETAILS,
            QUERY_CARD_NUMBER]