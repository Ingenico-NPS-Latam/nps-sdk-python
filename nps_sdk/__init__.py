from nps_sdk.configuration import Configuration
from nps_sdk.sdk import Nps
import os
os.environ['REQUESTS_CERT_NPS'] = os.path.dirname(__file__) + "/certs/sample.pem"
os.environ['REQUESTS_CERT_KEY'] = os.path.join(os.path.dirname(__file__)  + '/certs/','sample.key')