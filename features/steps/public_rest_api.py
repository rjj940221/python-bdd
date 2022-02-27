from behave import *
import requests
import re
import time
import datetime
import pytz
from requests.compat import urljoin
from src.api_tools.util import print_result

SERVER_TIME_PATH = '/0/public/Time'
ASSET_PAIR_PATH = '/0/public/AssetPairs'


@when('the server time is requested')
def step_impl(context):
    context.time_of_request = time.time()
    result = requests.get(urljoin(context.api_conf['url'], SERVER_TIME_PATH))
    context.result = result


@when('the asset pair "{asset_pair}" is requested')
def step_impl(context, asset_pair):
    context.time_of_request = time.time()
    result = requests.get(urljoin(context.api_conf['url'], ASSET_PAIR_PATH), params={"pair": asset_pair})
    context.result = result
    print_result(result)


@then('the response is not cached')
def step_impl(context):
    assert (re.match(r'.*no-cache.*', context.result.headers['cache-control']))
    assert 'CF-Cache-Status' in context.result.headers
    assert context.result.headers['CF-Cache-Status'] == 'MISS', f"Expected {context.result.headers['CF-Cache-Status']} to match MISS"


@then('the system time is in a margin of 1 sec')
def step_impl(context):
    assert (abs(context.time_of_request - context.body['result']['unixtime']) <= 1),  f"expected {abs(context.time_of_request - context.body['result']['unixtime'])} <= 1"


@then('the unixtime field corresponds with the rfc1123')
def step_impl(context):
    datetime.datetime.fromtimestamp(context.body['result']['unixtime']).astimezone(pytz.utc).strftime(
        '%a, %d %b %y %H:%M:%S +0000')


@then('the the response has a "{asset_pair}" section')
def step_impl(context, asset_pair):
    assert asset_pair in context.body['result'].keys()


@then('the the response "{asset_pair}" section is valid')
def step_impl(context, asset_pair):
    asset_pair = context.body['result'][asset_pair]
    obj_keys = asset_pair.keys()
    assert "altname" in obj_keys
    assert isinstance(asset_pair["altname"], str)
    assert "wsname" in obj_keys
    assert isinstance(asset_pair["wsname"], str)
    assert "aclass_base" in obj_keys
    assert isinstance(asset_pair["aclass_base"], str)
    assert "base" in obj_keys
    assert isinstance(asset_pair["base"], str)
    assert "aclass_quote" in obj_keys
    assert isinstance(asset_pair["aclass_quote"], str)
    assert "quote" in obj_keys
    assert isinstance(asset_pair["quote"], str)
    assert "lot" in obj_keys
    assert isinstance(asset_pair["lot"], str)
    assert "pair_decimals" in obj_keys
    assert isinstance(asset_pair["pair_decimals"], int)
    assert "lot_decimals" in obj_keys
    assert isinstance(asset_pair["lot_decimals"], int)
    assert "lot_multiplier" in obj_keys
    assert isinstance(asset_pair["lot_multiplier"], int)
    assert "leverage_buy" in obj_keys
    # TODO is there a minimum len to all lists?
    assert isinstance(asset_pair["leverage_buy"], list)
    assert "leverage_sell" in obj_keys
    assert isinstance(asset_pair["leverage_sell"], list)
    assert "fees" in obj_keys
    assert isinstance(asset_pair["fees"], list)
    assert "fees_maker" in obj_keys
    assert isinstance(asset_pair["fees_maker"], list)
    assert "fee_volume_currency" in obj_keys
    assert isinstance(asset_pair["fee_volume_currency"], str)
    assert "margin_call" in obj_keys
    assert isinstance(asset_pair["margin_call"], int)
    assert "margin_stop" in obj_keys
    assert isinstance(asset_pair["margin_stop"], int)
    assert "ordermin" in obj_keys
    assert isinstance(asset_pair["ordermin"], str)
