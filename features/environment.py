import os
from src.api_tools import api_conf


def before_all(context):
    if 'API_CONFIG_PATH' in os.environ:
        conf = api_conf.read_config(os.environ['API_CONFIG_PATH'])
    else:
        conf = api_conf.read_config()

    if 'url' not in conf or not conf['url'].startswith('https://'):
        raise ValueError("Config for api url was not found or was invalid")
    context.api_conf = conf
