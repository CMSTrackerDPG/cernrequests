import requests

from cernrequests.certs import default_user_certificate_paths, where


def get(url, params=None, **kwargs):
    if "cert" not in kwargs:
        kwargs["cert"] = default_user_certificate_paths()
    if "verify" not in kwargs:
        kwargs["verify"] = where()
    return requests.get(url, params=params, **kwargs)
