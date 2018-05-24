from nps_sdk.constants import PRODUCTION_ENV, STAGING_ENV, SANDBOX_ENV, DEVELOPMENT_ENV
from nps_sdk.errors import ApiException
import nps_sdk
import logging


merchant_id = "psp_test"
#merchant_id = "sdk_test"
#merchant_id = "365online"

nps_sdk.Configuration.configure(environment=SANDBOX_ENV,
                                # secret_key="swGYxNeehNO8fS1zgwvCICevqjHbXcwPWAvTVZ5CuULZwKWaGPmXbPSP8i1fKv2q", #sdk_test
                                secret_key="IeShlZMDk8mp8VA6vy41mLnVggnj1yqHcJyNqIYaRINZnXdiTfhF0Ule9WNAUCR6", #psp_test
                                #secret_key="xfMzDG2gDMwYABT3JWUmkH14i3uwXMTW2hI2GIomhxq3FORdhDs9EDSAeqRQJmMt", #365online
                                #secret_key="wDbxnRDvF3wmcETN9bih7j4R9FhC3PczaBuNd7JqAFalR38adqGiYKAfZpsbCSYm", #inclufin
                                #secret_key="0NdyJ37jbRqUnw5ATJoDbkq52WYv9BY8YC6qDCZodNIOJLYmcL0D5oG5Kp0R0WZZ",
                                log_level=logging.INFO, debug=True, cert_verify_peer=False, cert=False, timeout=30, cache=True, cache_location='/tmp', cache_ttl=86400, as_obj=True)


def run_create_client_session():
    """CreateClientSession"""

    sdk = nps_sdk.Nps()

    params = {
        'psp_Version': '2.2',
        'psp_MerchantId': merchant_id,
        'psp_PosDateTime': '2017-01-01 12:00:00'
    }
    resp = sdk.create_client_session(params)

    return resp



print(run_create_client_session())