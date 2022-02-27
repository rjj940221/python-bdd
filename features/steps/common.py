import re

from behave import *


@then('a valid JSON response is returned')
def step_impl(context):
    result = context.result
    assert result.status_code == 200
    assert (re.match(r'^application/json(?:;\s*charset=utf-(?:8|16))?$', result.headers['Content-Type']))
    context.body = result.json()


@then('the response has no error messages')
def step_impl(context):
    errors = context.body['error']
    assert (len(errors) == 0)


@then('the response has the error messages "{error_message}"')
def step_impl(context, error_message):
    errors = context.body['error']
    assert (len(errors) > 0)
    assert error_message in errors

