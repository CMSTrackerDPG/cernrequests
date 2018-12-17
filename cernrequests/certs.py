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

FALLBACK_BASE_PATH = "{}/.globus".format(os.getenv("HOME"))
DEFAULT_BASE_PATH = os.getenv("CERN_CERTIFICATE_PATH", FALLBACK_BASE_PATH)


def default_user_certificate_paths():
    """
    :return: (cert, key) tuple of CERN user certificates paths
    """
    cert = "{}/usercert.pem".format(DEFAULT_BASE_PATH)
    key = "{}/userkey.pem".format(DEFAULT_BASE_PATH)

    return cert, key


def where():
    """
    :return: CERN Root Certification Authority bundle path
    """
    folder = os.path.dirname(__file__)
    return os.path.join(folder, "cern-cacert.pem")
