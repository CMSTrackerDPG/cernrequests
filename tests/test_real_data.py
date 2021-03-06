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


def test_lumis():
    """
    The lumis website does not require the CERN Root Certificate Authority
    """
    url = "https://lumis.web.cern.ch/api/all/?run_min=323755&run_max=323755"
    expected = json.loads(
        '{"323755": [[27, 815], [816, 817], [818, 823], '
        "[824, 825], [826, 826], [827, 827], [828, 830], "
        "[831, 832], [833, 861], [862, 863], [864, 964], "
        "[965, 966]]}"
    )

    cookies = get_sso_cookies(url)
    response = requests.get(url, cookies=cookies)
    assert expected == response.json()


def test_wbm():
    """
    The CMS WBM webiste requires the CERN Root Certificate Authority
    """
    url = "https://cmswbm.cern.ch/cmsdb/servlet/RunSummary?RUN=211831&FORMAT=XML"
    cookies = get_sso_cookies(url, verify=False)
    response = cernrequests.get(url, cookies=cookies, verify=False)

    expected = "<nLumiSections>160</nLumiSections>"
    assert expected in response.text


def test_wbm_without_wrapper():
    url = "https://cmswbm.cern.ch/cmsdb/servlet/RunSummary?RUN=211831&FORMAT=XML"
    cookies = get_sso_cookies(url, verify=False)

    response = requests.get(url, cookies=cookies, verify=False)
    expected = "<nLumiSections>160</nLumiSections>"
    assert expected in response.text

    # Missing Certification Authority
    with pytest.raises(SSLError):
        requests.get(url, cookies=cookies)

    # Missing Grid User Certificate
    response = requests.get(url, verify=False)
    assert expected not in response.text
