"""
API Token getter, based on
https://gitlab.cern.ch/authzsvc/docs/api-access-examples/-/blob/master/python/api_token.py
"""

import logging
import datetime
import requests
import jwt

DEFAULT_SERVER = "auth.cern.ch"
DEFAULT_REALM = "cern"
DEFAULT_REALM_PREFIX = "auth/realms/{}"
DEFAULT_TOKEN_ENDPOINT = "api-access/token"


def get_token_endpoint(server=DEFAULT_SERVER, realm=DEFAULT_REALM):
    """
    Gets the token enpdoint path from the args
    """
    return "https://{}/{}/{}".format(
        server, DEFAULT_REALM_PREFIX.format(realm), DEFAULT_TOKEN_ENDPOINT
    )


def get_api_token(
    client_id, client_secret, target_application, token_endpoint=get_token_endpoint()
):
    logging.debug(
        "[x] Getting API token as {} for {}".format(client_id, target_application)
    )

    r = requests.post(
        token_endpoint,
        auth=(client_id, client_secret),
        data={"grant_type": "client_credentials", "audience": target_application},
    )

    if not r.ok:
        msg = "ERROR getting token: {}".format(r.json())
        logging.error(msg)
        raise Exception(msg)

    response_json = r.json()
    token = response_json["access_token"]
    expires_in_seconds = response_json["expires_in"]
    expiration_datetime = datetime.datetime.now() + datetime.timedelta(
        seconds=expires_in_seconds
    )

    # logging.debug(jwt.decode(token, verify=False))
    logging.debug("[x] Token obtained")

    return token, expiration_datetime
