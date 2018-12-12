import os

import requests


def default_user_certificate_paths():
    home_path = os.getenv("HOME")
    cert = "{}/private/usercert.pem".format(home_path)
    key = "{}/private/userkey.pem".format(home_path)

    assert os.path.isfile(cert)
    assert os.path.isfile(key)
    return cert, key


def root_certificate_path():
    folder = os.path.dirname(__file__)
    return os.path.join(folder, 'CERN-bundle.pem')


def get(url, params=None, **kwargs):
    if "cert" not in kwargs:
        kwargs["cert"] = default_user_certificate_paths()
    if "verify" not in kwargs:
        kwargs["verify"] = root_certificate_path()
    return requests.get(url, params=params, **kwargs)
