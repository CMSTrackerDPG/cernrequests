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
import requests

import cernrequests
from cernrequests import certs
from cernrequests.cookies import get_sso_cookies
from cernrequests.core import get, get_with_token


def test_dqmgui():
    """
    The DQM GUI does not require cookies, but does require Grid User Certificates
    :return:
    """
    url = "https://cmsweb.cern.ch/dqm/offline/jsonfairy/archive/321012/StreamExpress/Run2018D-Express-v1/DQMIO/"
    expected = json.loads('{"hist": "unsupported type"}')

    assert expected == cernrequests.get(url).json()


def test_rr():
    """
    RunRegistry requires cookies
    """

    url = (
        "https://dev-cmsrunregistry.web.cern.ch/api/get_all_dataset_names_of_run/357756"
    )
    response = get_with_token(
        url, target_application="dev-cmsrunregistry-sso-proxy"
    ).json()
    expected = [
        # TODO: Uncomment this when new SSO is deployed for production RR
        # "/Express/Collisions2022/DQM",
        # "/Express/Commissioning2022/DQM",
        "online",
        # "/PromptReco/Collisions2022/DQM",
    ]

    assert expected == response
