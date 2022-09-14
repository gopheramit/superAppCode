import json
import random
import string
import hmac
import base64
import hashlib
import time
import requests

base_url = 'https://sandboxapi.rapyd.net'
secret_key = '672d23cd5b3c8602c472bceaab2d17323c6ac92e13a61e0e8d099756f622994cb394f3a1f2de7d5e'
access_key = '94FBABD5DA7F959BC979'

def generate_salt(length=12):
    return ''.join(random.sample(string.ascii_letters + string.digits, length))

def get_unix_time(days=0, hours=0, minutes=0, seconds=0):
    return int(time.time())

def update_timestamp_salt_sig(http_method, path, body):
    if path.startswith('http'):
        path = path[path.find(f'/v1'):]
    salt = generate_salt()
    timestamp = get_unix_time()
    #body="""{"metadata":{"user_defined":"silver"},"merchant_reference_id":"12345689","payments":[{"amount":"5","currency":"USD","payment_method":{"type":"sg_debit_visa_card","fields":{"number":"4111111111111111","expiration_month":"10","expiration_year":"23","cvv":"123","name":"Rivers"}},"ewallets":[{"ewallet":"ewallet_f49f45152f2081fbccf70052fdd8c9c0"}]},{"amount":"2","currency":"USD","payment_method":{"type":"sg_debit_visa_card","fields":{"number":"4111111111111111","expiration_month":"10","expiration_year":"23","cvv":"123","name":"Henderson"}},"ewallets":[{"ewallet":"ewallet_ad689618491a6161f5c2e49dcf4aa156"}]}]}"""
    to_sign = (http_method, path, salt, str(timestamp), access_key, secret_key, body)
    
    h = hmac.new(secret_key.encode('utf-8'), ''.join(to_sign).encode('utf-8'), hashlib.sha256)
    signature = base64.urlsafe_b64encode(str.encode(h.hexdigest()))
    return salt, timestamp, signature

def current_sig_headers(salt, timestamp, signature):
    sig_headers = {'access_key': access_key,
                   'salt': salt,
                   'timestamp': str(timestamp),
                   'signature': signature,
                   'idempotency': str(get_unix_time()) + salt}
    return sig_headers

def pre_call(http_method, path, body=None):
    str_body = json.dumps(body, separators=(',', ':'), ensure_ascii=False) if body else ''
    #str_body = body
    print(str_body,"str_body")
    salt, timestamp, signature = update_timestamp_salt_sig(http_method=http_method, path=path, body=str_body)
    return str_body.encode('utf-8'), salt, timestamp, signature

def create_headers(http_method, url,  body=None):
    body, salt, timestamp, signature = pre_call(http_method=http_method, path=url, body=body)
    return body, current_sig_headers(salt, timestamp, signature)

def make_request(method,path,body=''):
    #print(body,"beofre call")
    body, headers = create_headers(method, base_url + path, body)
    #print(body,"body for call")
    #body="""{"metadata":{"user_defined":"silver"},"merchant_reference_id":"12345689","payments":[{"amount":"5","currency":"USD","payment_method":{"type":"sg_debit_visa_card","fields":{"number":"4111111111111111","expiration_month":"10","expiration_year":"23","cvv":"123","name":"Rivers"}},"ewallets":[{"ewallet":"ewallet_f49f45152f2081fbccf70052fdd8c9c0"}]},{"amount":"2","currency":"USD","payment_method":{"type":"sg_debit_visa_card","fields":{"number":"4111111111111111","expiration_month":"10","expiration_year":"23","cvv":"123","name":"Henderson"}},"ewallets":[{"ewallet":"ewallet_ad689618491a6161f5c2e49dcf4aa156"}]}]}"""

    if method == 'get':
        response = requests.get(base_url + path,headers=headers)
    elif method == 'put':
        response = requests.put(base_url + path, data=body, headers=headers)
    elif method == 'delete':
        response = requests.delete(base_url + path, data=body, headers=headers)
    else:
        response = requests.post(base_url + path, data=body, headers=headers)
        print(response,"post")

    if response.status_code != 200:
        raise TypeError(response, method,base_url + path)
    return json.loads(response.content)