#!/usr/bin/python
# -*- coding: utf-8 -*-

# © Copyright 2023 CERN
#
# This software is distributed under the terms of the GNU Lesser General Public
# Licence version 3 (LGPL Version 3), copied verbatim in the file “LICENSE”
#
# In applying this licence, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as an Intergovernmental Organization
# or submit itself to any jurisdiction.
__version__ = "0.4.2"

from .core import get, get_with_token
from .token import get_api_token
from .cookies import get_sso_cookies
