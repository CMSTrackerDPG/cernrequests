[![Build Status](https://travis-ci.com/CMSTrackerDPG/cernrequests.svg?branch=master)](https://travis-ci.com/CMSTrackerDPG/cernrequests)
[![](https://img.shields.io/pypi/v/cernrequests.svg)](https://pypi.org/project/cernrequests/)


# CERN Requests

Enables using [requests]("https://github.com/requests/requests") without having to configure the CERN Root certificates.

Inspired by [certifi](https://github.com/certifi/python-certifi), [requests-kerberos](https://github.com/requests/requests-kerberos) and [cern-sso-python](https://github.com/cerndb/cern-sso-python)

The Root certificate bundle is copied from the [linuxsoft cern page](http://linuxsoft.cern.ch/cern/centos/7/cern/x86_64/repoview/CERN-CA-certs.html) and can also be created manually by downloading the CERN Grid Certification Authority files from [cafiles.cern.ch/cafiles](https://cafiles.cern.ch/cafiles/).

## Installation

Requires ```Python 2.7``` or ```Python 3.4+```

```bash
pip install cernrequests
```

## Prerequisites

Request a [Grid User Certificate](https://ca.cern.ch/ca/) and convert into public and private key:

```bash
mkdir -p ~/private
openssl pkcs12 -clcerts -nokeys -in myCertificate.p12 -out ~/private/usercert.pem
openssl pkcs12 -nocerts -in myCertificate.p12 -out ~/private/userkey.tmp.pem
openssl rsa -in ~/private/userkey.tmp.pem -out ~/private/userkey.pem
```

The certificates have to be **passwordless**.

## Usage

### Example

```python
import cernrequests

url = "https://<your-cern-website>"
response = cernrequests.get(url)
```

### Cookies Example

If you want to access a website which requires CERN Single Sign-on cookies you can do the following:

```python
import cernrequests

url = "https://<your-cern-website>"
cookies = cernrequests.get_sso_cookies(url)
response = cernrequests.get(url, cookies=cookies)
```

### Alternative usage

If you want to use ```requests``` directly without the CERN wrapper you can get the exact same functionality by doing:

```python
import requests
from cernrequests import certs

url = "https://<your-cern-website>"
cert = certs.default_user_certificate_paths()
ca_bundle = certs.where()

response = requests.get(url, cert=cert, verify=ca_bundle)
```

## Configuration

The default user certificate paths are first ```~\private\``` and ```~\.globus\``` for fallback. The default *public* key file name is ```usercert.pem``` and the default *private* key file name is ```userkey.pem```

You can configure the default grid user certificate path by setting the ```CERN_CERTIFICATE_PATH``` environment variable.

For example:

```bash
export CERN_CERTIFICATE_PATH=${HOME}/my_custom_folder
```

This will still assume that your filenames are ```usercert.pem``` and ```userkey.pem```
Write this line in your ```.bashrc``` to make the configuration persistent.

Alternatively you can also specify the paths directly in your code:

```python
import cernrequests

url = "https://<your-cern-website>"
cert = "my/custom/path/cert.pem"    # Public key path
key = "my/custom/path/key.pem"      # Private key path

cernrequests.get(url, cert=(cert,key))
```

This way you can even use custom names such as ```cert.pem``` and ```key.pem```

## Testing

```bash
python -m venv venv
source venv/bin/activate
pip install -r testing-requirements.txt
pytest
```

## FAQ

### I'm getting `certificate verify failed`! What should I do?

The `cernrequests/cern-cacerts.pem` file has expired, and will need to be updated by the library maintainer. Download all the CA files from [here](https://ca.cern.ch/cafiles/certificates/Download.aspx?ca=cern) and convert them to `.pem` files, one-by-one by running:

```bash
 openssl x509 -in <CERN certification authority file.crt> -out temp.pem -outform PEM
```

Then, merge the contents of each `.pem` file into a single `cern-cacerts.pem` file and replace the existing one. Verify that the certs work by running `pytest`.

## References

- http://docs.python-requests.org/en/master/
- https://certifi.io/en/latest/
- https://github.com/cerndb/cern-sso-python
- https://linux.web.cern.ch/linux/docs/cernssocookie.shtml
- http://linuxsoft.cern.ch/cern/centos/7/cern/x86_64/repoview/CERN-CA-certs.html
- https://ca.cern.ch/ca/
