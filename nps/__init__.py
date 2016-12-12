from nps.configuration import Configuration
from nps.nps_sdk import NpsSDK
import os
os.environ['REQUESTS_CERT_NPS'] = os.path.dirname(__file__) + "/certs/sample.pem"
os.environ['REQUESTS_CERT_KEY'] = os.path.join(os.path.dirname(__file__)  + '/certs/','sample.key')