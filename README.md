[![Build Status](https://travis-ci.com/ptrstn/cernrequests.svg?branch=master)](https://travis-ci.com/ptrstn/cernrequests)

# CERN Requests

Enables using [requests]("https://github.com/requests/requests") without having to configure the CERN Root certificates.

Inspired by [certifi](https://github.com/certifi/python-certifi), [requests-kerberos](https://github.com/requests/requests-kerberos) and [cern-sso-python](https://github.com/cerndb/cern-sso-python)

The Root certificate bundle is copied from the [linuxsoft cern page](http://linuxsoft.cern.ch/cern/centos/7/cern/x86_64/repoview/CERN-CA-certs.html) and can also be created manually by downloading the CERN Grid Certification Authority files from [cafiles.cern.ch/cafiles](https://cafiles.cern.ch/cafiles/).

## Installation

Requires ```Python 2.7``` or ```Python 3.4+```

```bash
pip intall git+https://github.com/ptrstn/cernrequests
```

## Prerequisites

Request a [Grid User Certificate](https://ca.cern.ch/ca/) and convert into public and private key:

```bash
mkdir -p ~/.globus
openssl pkcs12 -clcerts -nokeys -in myCertificate.p12 -out ~/.globus/usercert.pem
openssl pkcs12 -nocerts -in myCertificate.p12 -out ~/.globus/userkey.tmp.pem
openssl rsa -in ~/.globus/userkey.tmp.pem -out ~/.globus/userkey.pem
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

If you want to access a website which requires which CERN Single Sign-on cookies you can do the following:

```python
import cernrequests

url = "https://<your-cern-website>"
cookies = cernrequests.get_sso_cookies(url)
response = cernrequests.get(url, cookies=cookies)
```

## FAQ

### How do i specify custom user certificate paths?

The default user certificate paths are ```~\.globus\usercert.pem``` and ```~\.globus\userkey.pem```. 

If you want to use different paths you can pass them to the cert argument:

```python
import cernrequests

url = "https://<your-cern-website>"
cert = "my/custom/path/cert.pem"    # Public key path
key = "my/custom/path/key.pem"      # Private key path

cernrequests.get(url, cert=(cert,key))
```

## References

- http://docs.python-requests.org/en/master/
- https://certifi.io/en/latest/
- https://github.com/cerndb/cern-sso-python
- https://linux.web.cern.ch/linux/docs/cernssocookie.shtml
- http://linuxsoft.cern.ch/cern/centos/7/cern/x86_64/repoview/CERN-CA-certs.html
- https://ca.cern.ch/ca/