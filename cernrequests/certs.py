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
