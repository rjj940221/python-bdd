import configparser
import logging
import os


def read_config(config_path='/opt/bdd/api_config.ini'):
    config = configparser.ConfigParser()
    if os.path.exists(config_path):
        config.read(config_path)
    else:
        logging.warning(f"Config file {config_path} not fund")
    if 'api' not in config:
        config['api'] = {}

    if 'API_2FA' in os.environ:
        config['api']['2FA'] = os.environ['API_2FA']
    if 'API_PUBLIC_KEY' in os.environ:
        config['api']['public_key'] = os.environ['API_PUBLIC_KEY']
    if 'API_PRIVATE_KEY' in os.environ:
        config['api']['private_key'] = os.environ['API_PRIVATE_KEY']
    if 'API_URL' in os.environ:
        config['api']['url'] = os.environ['API_URL']

    api_conf = config['api']

    return api_conf