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

import json
import pytest

import requests
from requests.exceptions import SSLError

import cernrequests
from cernrequests import certs
from cernrequests.cookies import get_sso_cookies


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
    url = "https://cmsrunregistry.web.cern.ch/api/get_all_dataset_names_of_run/357756"
    cert = certs.default_user_certificate_paths()
    ca_bundle = certs.where()
    cookies = get_sso_cookies(url, cert, verify=ca_bundle)
    response = requests.get(url, cookies=cookies).json()
    expected = [
        "/Express/Collisions2022/DQM",
        "/Express/Commissioning2022/DQM",
        "online",
        "/PromptReco/Collisions2022/DQM",
    ]

    assert expected == response
