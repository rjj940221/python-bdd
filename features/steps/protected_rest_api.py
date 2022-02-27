import random
import string
import time
import onetimepass as otp_gen
import requests
from requests.compat import urljoin
from behave import *
from src.api_tools import api_auth
from src.api_tools.util import print_result

OPEN_ORDER_PATH = '/0/private/OpenOrders'


def request_signature(uri_path, data, api_key, api_sec):
    return {'API-Key': api_key, 'API-Sign': api_auth.get_api_signature(uri_path, data, api_sec)}


def validate_order_description(order_desc):
    obj_keys = order_desc.keys()
    assert 'pair' in obj_keys
    assert isinstance(order_desc['pair'], str)
    assert 'type' in obj_keys
    assert isinstance(order_desc['type'], str)
    assert order_desc['type'] in ["buy", "sell"]
    assert 'ordertype' in obj_keys
    assert isinstance(order_desc['ordertype'], str)
    assert order_desc['ordertype'] in ["market", "limit", "stop-loss", "take-profit", "stop-loss-limit",
                                       "take-profit-limit", "settle-position"]
    assert 'price' in obj_keys
    assert isinstance(order_desc['price'], str)
    assert 'price2' in obj_keys
    assert isinstance(order_desc['price2'], str)
    assert 'leverage' in obj_keys
    assert isinstance(order_desc['leverage'], str)
    assert 'order' in obj_keys
    assert isinstance(order_desc['order'], str)
    assert 'close' in obj_keys
    assert isinstance(order_desc['close'], str)


def validate_order(order):
    obj_keys = order.keys()

    assert "refid" in obj_keys
    assert isinstance(order["refid"], str)
    assert "userref" in obj_keys
    assert isinstance(order["userref"], str)
    assert "status" in obj_keys
    assert isinstance(order["status"], str)
    assert "opentm" in obj_keys
    assert isinstance(order["opentm"], float) | isinstance(order["opentm"], int)
    assert "starttm" in obj_keys
    assert isinstance(order["starttm"], float) | isinstance(order["starttm"], int)
    assert "expiretm" in obj_keys
    assert isinstance(order["expiretm"], float) | isinstance(order["expiretm"], int)
    assert "descr" in obj_keys
    validate_order_description(order["descr"])
    assert "vol" in obj_keys
    assert isinstance(order["vol"], str)
    assert "vol_exec" in obj_keys
    assert isinstance(order["vol_exec"], str)
    assert "cost" in obj_keys
    assert isinstance(order["cost"], str)
    assert "fee" in obj_keys
    assert isinstance(order["fee"], str)
    assert "price" in obj_keys
    assert isinstance(order["price"], str)
    assert "stopprice" in obj_keys
    assert isinstance(order["stopprice"], str)
    assert "limitprice" in obj_keys
    assert isinstance(order["limitprice"], str)
    assert "misc" in obj_keys
    assert isinstance(order["misc"], str)
    assert "trigger" in obj_keys
    assert isinstance(order["trigger"], str)
    assert "oflags" in obj_keys
    assert isinstance(order["oflags"], str)


def get_signature_details(context):
    nonce = ""
    otp = None
    public_key = ""
    private_key = ""

    if hasattr(context, 'nonce'):
        nonce = context.nonce
    if hasattr(context, 'TwoFA'):
        otp = otp_gen.get_totp(context.TwoFA, as_string=True)
    if hasattr(context, 'public_key'):
        public_key = context.public_key
    if hasattr(context, 'private_key'):
        private_key = context.private_key

    return nonce, otp, public_key, private_key


@given('valid api keys')
def step_impl(context):
    if not hasattr(context, 'api_conf'):
        raise ValueError('api config not found')
    if context.api_conf['public_key'] is None:
        raise ValueError('"public_key" not found in config')
    if context.api_conf['private_key'] is None:
        raise ValueError('"private_key" not found in config')

    context.public_key = context.api_conf['public_key']
    context.private_key = context.api_conf['private_key']


@given('a valid api public keys')
def step_impl(context):
    if not hasattr(context, 'api_conf'):
        raise ValueError('api config not found')
    if context.api_conf['public_key'] is None:
        raise ValueError('"public_key" not found in config')

    context.public_key = context.api_conf['public_key']


@given('a valid api private keys')
def step_impl(context):
    if not hasattr(context, 'api_conf'):
        raise ValueError('api config not found')
    if context.api_conf['private_key'] is None:
        raise ValueError('"private_key" not found in config')

    context.private_key = context.api_conf['private_key']


@given('random api keys')
def step_impl(context):
    options = string.ascii_letters + string.digits

    context.public_key = ''.join(random.choice(options) for _ in range(58))
    context.private_key = ''.join(random.choice(options) for _ in range(88))


@given('a random api public keys')
def step_impl(context):
    options = string.ascii_letters + string.digits

    context.public_key = ''.join(random.choice(options) for _ in range(58))


@given('a random api private keys')
def step_impl(context):
    options = string.ascii_letters + string.digits

    context.private_key = ''.join(random.choice(options) for _ in range(88))


@given('a valid 2FA key')
def step_impl(context):
    if not hasattr(context, 'api_conf'):
        raise ValueError('api config not found')
    if context.api_conf['2FA'] is None:
        raise ValueError('"2FA" not found in config')
    context.TwoFA = context.api_conf['2FA']


@given('a random 2FA key')
def step_impl(context):
    options = 'AIQYBJRZCKS2DLT3EMU4FNV5GOW6HPX7'

    context.TwoFA = ''.join(random.choice(options) for _ in range(24))


@given('a valid nonce')
def step_impl(context):
    context.nonce = str(int(1000 * time.time()))


@given('account open orders are requested with a singed request')
def step_impl(context):
    nonce, otp, public_key, private_key = get_signature_details(context)
    data = {
        "nonce": nonce,
        "otp": otp,
        "trades": False
    }
    headers = request_signature(OPEN_ORDER_PATH, data, public_key, private_key)
    context.request_body = data
    context.request_headers = headers
    requests.post(urljoin(context.api_conf['url'], OPEN_ORDER_PATH), headers=headers, data=data)


@when('account open orders are requested with a singed request')
def step_impl(context):
    nonce, otp, public_key, private_key = get_signature_details(context)
    data = {
        "nonce": context.nonce,
        "otp": otp,
        "trades": False
    }
    headers = request_signature(OPEN_ORDER_PATH, data, public_key, private_key)
    result = requests.post(urljoin(context.api_conf['url'], OPEN_ORDER_PATH), headers=headers, data=data)
    context.result = result
    print_result(result)


@when('the request is repeated')
def step_impl(context):
    result = requests.post(urljoin(context.api_conf['url'], OPEN_ORDER_PATH),
                           headers=context.request_headers,
                           data=context.request_body)
    context.result = result

    print_result(result)


@when('account open orders are requested')
def step_impl(context):
    data = {
        "nonce": 0,
        "trades": False
    }
    result = requests.post(urljoin(context.api_conf['url'], OPEN_ORDER_PATH), data=data)
    context.result = result

    print_result(result)


@then('the response has 0 or more orders')
def step_impl(context):
    body = context.body
    assert 'result' in body
    assert 'open' in body['result']
    assert len(body['result']['open'].keys()) >= 0
    if len(body['result']['open'].keys()) > 0:
        for order_key in body['result']['open']:
            validate_order(body['result']['open'][order_key])
