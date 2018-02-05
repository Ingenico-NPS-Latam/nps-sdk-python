#  Python SDK
 

## Availability
Supports Python 2.6, 2.7, 3.3, 3.4 and 3.5


## How to install

```
pip install nps_sdk
```

## Configuration

It's a basic configuration of the SDK

```python
import nps_sdk
from nps_sdk.constants import SANDBOX_ENV

nps_sdk.Configuration.configure(environment=SANDBOX_ENV, secret_key="_YOUR_SECRET_KEY_")
```



Here is an simple example request:

```python
from nps_sdk.errors import ApiException
import nps_sdk

sdk = nps_sdk.Nps()
params = {
    "psp_Version": '2.2',
    "psp_MerchantId": 'psp_test',
    "psp_TxSource": 'WEB',
    "psp_MerchTxRef": 'ORDER69461-3',
    "psp_MerchOrderId": 'ORDER69461',
    "psp_Amount": '15050',
    "psp_NumPayments": '1',
    "psp_Currency": '032',
    "psp_Country": 'ARG',
    "psp_Product": '14',
    "psp_CardNumber": '4507990000000010',
    "psp_CardExpDate": '1612',
    "psp_PosDateTime": '2016-12-01 12:00:00',
    "psp_CardSecurityCode": '123'
}
try:
    resp = sdk.pay_online_2p(params)
except ApiException as e:
    #Code to handle error
    pass
```

## Environments

```python
import nps_sdk
from nps_sdk.constants import PRODUCTION_ENV, STAGING_ENV, SANDBOX_ENV
```

## Error handling

ApiException: This exception is raised when a ReadTimeout or a ConnectTimeout occurs.

Note: The rest of the exceptions that can occur will be detailed inside of the response provided by NPS or will be provided by suds.

```python
from nps_sdk.errors import ApiException

#Code
try:
    #code or sdk call
except ApiException as e:
    #Code to handle error
    pass
```

## Advanced configurations

Nps SDK allows you to log what’s happening with you request inside of our SDK, it logs by default to stout.

```python
import nps_sdk
nps_sdk.Configuration.configure(secret_key="_YOUR_SECRET_KEY_", debug=True)
```


If you have the debug option enabled, the sdk can write the output generated from the logger to the file you provided.

```python
import nps_sdk
nps_sdk.Configuration.configure(secret_key="_YOUR_SECRET_KEY_", debug=True, log_file=”path/to/your/file.log”)
```

The logging.INFO level will write concise information of the request and will mask sensitive data of the request. 
The logging.DEBUG level will write information about the request to let developers debug it in a more detailed way.

```python
import nps_sdk
import logging
nps_sdk.Configuration.configure(secret_key="_YOUR_SECRET_KEY_", debug=True, log_level=logging.DEBUG)
```

Sanitize allows the SDK to truncate to a fixed size some fields that could make request fail, like extremely long name.

```python
import nps_sdk
nps_sdk.Configuration.configure(secret_key="_YOUR_SECRET_KEY_", sanitize=True)
```

you can change the timeout of the request.

```python
import nps_sdk
nps_sdk.Configuration.configure(secret_key="_YOUR_SECRET_KEY_",  timeout=60)
```

Proxy configuration

```python
import nps_sdk
from nps_sdk.utils import Proxy
proxy = Proxy(protocol="http", url = "http://__YOUR_PROXY_URL", port="3128", user="_YOUR_USER_", password="_YOUR_PASSWORD")
nps_sdk.Configuration.configure(secret_key="_YOUR_SECRET_KEY_", proxy = proxy)
```

Cache

```python
import nps_sdk
from nps_sdk.utils import Proxy
nps_sdk.Configuration.configure(environment=SANDBOX_ENV, secret_key="_YOUR_SECRET_KEY_", cache=True, cache_location='/tmp', cache_duration=86400) #seconds
```