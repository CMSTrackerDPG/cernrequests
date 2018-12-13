import json

import requests

import cernrequests
from cernrequests.cookies import get_sso_cookies


def test_dqmgui():
    url = "https://cmsweb.cern.ch/dqm/offline/jsonfairy/archive/321012/StreamExpress/Run2018D-Express-v1/DQMIO/"
    expected = json.loads('{"hist": "unsupported type"}')

    assert expected == cernrequests.get(url).json()


"""
def test_get_cookie():
    url = "https://lumis.web.cern.ch/api/all/?run_min=323755&run_max=323755"

    cert, key = cernrequests.core.default_user_certificate_paths()
    cookie = cern_sso.cert_sign_on(url, cert, key)

    # requests.get(url, cookies=cookie)
"""


def test_lumis():
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
    url = "https://cmswbm.cern.ch/cmsdb/servlet/LhcMonitor?FORMAT=XML"
    cookies = get_sso_cookies(url)
    response = cernrequests.get(url, cookies=cookies)
    print(response.content)
