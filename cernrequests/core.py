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

import requests

from cernrequests.certs import default_user_certificate_paths, where


def get(url, params=None, **kwargs):
    if "cert" not in kwargs:
        kwargs["cert"] = default_user_certificate_paths()
    if "verify" not in kwargs:
        kwargs["verify"] = where()
    return requests.get(url, params=params, **kwargs)
