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

CERT_PATH_ENVIRON_NAME = "CERN_CERTIFICATE_PATH"
DEFAULT_CERT_FILE_NAME = "usercert.pem"
DEFAULT_KEY_FILE_NAME = "userkey.pem"

_HOME = os.getenv("HOME")
PRIMARY_FALLBACK_BASE_PATH = os.path.join(_HOME, "private")
SECONDARY_FALLBACK_BASE_PATH = os.path.join(_HOME, ".globus")


class CertificateNotFound(Exception):
    pass


def _user_certs(base):
    """
    :return: CERN user certificate paths
    """
    cert = os.path.join(base, DEFAULT_CERT_FILE_NAME)
    key = os.path.join(base, DEFAULT_KEY_FILE_NAME)
    return cert, key


def _certificates_exist(base_path):
    """
    Check existence of user certificates in base_path
    """
    cert, key = _user_certs(base_path)
    return os.path.isfile(cert) and os.path.isfile(key)


def _base_path():
    """
    :return: Base path for CERN user certificates
    """
    base_path = os.getenv(CERT_PATH_ENVIRON_NAME)

    if base_path is not None:
        if _certificates_exist(base_path):
            return base_path
        message = (
            "{} environment variable is set, but CERN certificates '{}' and '{}' "
            "do not exist in '{}'".format(
                CERT_PATH_ENVIRON_NAME,
                DEFAULT_CERT_FILE_NAME,
                DEFAULT_KEY_FILE_NAME,
                base_path,
            )
        )
        raise CertificateNotFound(message)

    return _fallback_base_path()


def _fallback_base_path():
    """
    :return: Fallback base path for CERN user certificates
    """
    if _certificates_exist(PRIMARY_FALLBACK_BASE_PATH):
        return PRIMARY_FALLBACK_BASE_PATH

    if _certificates_exist(SECONDARY_FALLBACK_BASE_PATH):
        return SECONDARY_FALLBACK_BASE_PATH

    message = "CERN certificates '{}' and '{}' do not exist in '{}' or '{}'".format(
        DEFAULT_CERT_FILE_NAME,
        DEFAULT_KEY_FILE_NAME,
        PRIMARY_FALLBACK_BASE_PATH,
        SECONDARY_FALLBACK_BASE_PATH,
    )

    raise CertificateNotFound(message)


def default_user_certificate_paths():
    """
    :return: (cert, key) tuple of CERN user certificates paths
    """
    return _user_certs(_base_path())


def where():
    """
    :return: CERN Root Certification Authority bundle path
    """
    folder = os.path.dirname(__file__)
    return os.path.join(folder, "cern-cacert.pem")
