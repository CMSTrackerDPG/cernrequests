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
import json
from datetime import datetime
import cernrequests

RR_URL = "https://cmsrunregistry-qa.web.cern.ch/api/get_all_dataset_names_of_run/357756"


def test_get_with_certs():
    """
    The DQM GUI does not require token authentication, but does require Grid User Certificates
    :return:
    """
    url = "https://cmsweb.cern.ch/dqm/offline/jsonfairy/archive/321012/StreamExpress/Run2018D-Express-v1/DQMIO/"
    expected = json.loads('{"hist": "unsupported type"}')

    assert expected == cernrequests.get(url).json()


def test_get_with_token():
    """
    Test to check that not having a token at hand and using get_with_token
    works.

    RunRegistry requires token authentication.
    """

    # TODO: Update this URL when new SSO is deployed for production RR

    response = cernrequests.get_with_token(
        RR_URL, target_application="cmsrunregistry-sso-proxy"
    ).json()
    expected = [
        "/Express/Collisions2022/DQM",
        "/Express/Commissioning2022/DQM",
        "online",
        "/PromptReco/Collisions2022/DQM",
    ]

    assert expected == response


def test_get_api_token_and_get_with_token():
    """
    Test that gets a token and then uses it, to verify its reusability.
    """

    token, expires = cernrequests.get_api_token(
        client_id=os.environ.get("SSO_CLIENT_ID"),
        client_secret=os.environ.get("SSO_CLIENT_SECRET"),
        target_application="cmsrunregistry-sso-proxy",
    )
    assert token
    assert expires > datetime.now()

    response = cernrequests.get_with_token(
        url=RR_URL, target_application="cmsrunregistry-sso-proxy", api_token=token
    ).json()
    expected = [
        "/Express/Collisions2022/DQM",
        "/Express/Commissioning2022/DQM",
        "online",
        "/PromptReco/Collisions2022/DQM",
    ]

    assert expected == response
