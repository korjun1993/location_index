import os


def es_client():
    env = os.environ['PROFILE']

    if env == 'dev':
        return {
            "hosts": '',
            "username": '',
            "password": ''
        }
    elif env == 'stg':
        return {
            "hosts": '',
            "username": '',
            "password": ''
        }
    elif env == 'live':
        return {
            "hosts": '',
            "username": '',
            "password": ''
        }

    raise Exception('Invalid environment')
