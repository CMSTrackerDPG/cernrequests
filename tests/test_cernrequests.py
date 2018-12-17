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
import cernrequests
from cernrequests.certs import where, default_user_certificate_paths


def test_cernrequests():
    url = "https://jsonplaceholder.typicode.com/todos/1"

    expected = json.loads(
        """{
          "userId": 1,
          "id": 1,
          "title": "delectus aut autem",
          "completed": false
        }"""
    )

    assert expected == cernrequests.get(url, cert=None, verify=True).json()


def test_invalid_certificate():
    fake_certs = ("bla", "blub")
    url = "https://jsonplaceholder.typicode.com/todos/1"

    with pytest.raises(IOError):
        cernrequests.get(url, cert=fake_certs)


def test_default_user_certificate_paths():
    cert, key = default_user_certificate_paths()

    assert "usercert.pem" in cert
    assert "userkey.pem" in key


def test_root_certificate_path():
    cert = where()

    assert "cern-cacert.pem" in cert
