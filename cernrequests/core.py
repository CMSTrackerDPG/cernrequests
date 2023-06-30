#!/usr/bin/python
# -*- coding: utf-8 -*-

# © Copyright 2018 CERN
#
# This software is distributed under the terms of the GNU Lesser General Public
# Licence version 3 (LGPL Version 3), copied verbatim in the file “LICENSE”
#
# In applying this licence, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as an Intergovernmental Organization
# or submit itself to any jurisdiction.

import os
import requests
from dotenv import load_dotenv
from cernrequests.token import get_api_token
from cernrequests.certs import default_user_certificate_paths, where

load_dotenv()


def get(url, params=None, **kwargs):
    """
    Method working with Grid Credentials.

    Note: this is no longer supported by the "new"
    CERN SSO (2023/06).

    This method can still be used with CMSWEB.
    """
    if "cert" not in kwargs:
        kwargs["cert"] = default_user_certificate_paths()
    if "verify" not in kwargs:
        kwargs["verify"] = where()
    return requests.get(url, params=params, **kwargs)


def get_with_token(url, params=None, **kwargs):
    """
    Method working with the new (2023/06) SSO.
    """
    if "target_application" not in kwargs:
        raise Exception("You must specify the target_application")
    target_application = kwargs.pop("target_application")
    client_id = os.environ.get("SSO_CLIENT_ID")
    client_secret = os.environ.get("SSO_CLIENT_SECRET")
    api_token, expiration_datetime = get_api_token(
        client_id=client_id,
        client_secret=client_secret,
        target_application=target_application,
    )
    return requests.get(
        url,
        params=params,
        headers={
            "Authorization": "Bearer " + api_token,
            "Content-Type": "application/json",
        },
        **kwargs
    )
