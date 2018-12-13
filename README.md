[![Build Status](https://travis-ci.com/ptrstn/cernrequests.svg?branch=master)](https://travis-ci.com/ptrstn/cernrequests)

# CERN Requests

Enables using [requests]("https://github.com/requests/requests") without having to configure the CERN Root certificates.

Inspired by [certifi](https://github.com/certifi/python-certifi) and [requests-kerberos](https://github.com/requests/requests-kerberos)

The Root certificate bundle is copied from the [linuxsoft cern page](http://linuxsoft.cern.ch/cern/centos/7/cern/x86_64/repoview/CERN-CA-certs.html) and can also be created manually by downloading the CERN Grid Certification Authority files from [cafiles.cern.ch/cafiles](https://cafiles.cern.ch/cafiles/).

## Installation

Requires ```Python 2.7``` or ```Python 3.4+```

```bash
pip intall git+https://github.com/ptrstn/cernrequests
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

## Example Usage

```python
import cernrequests

url = "https://cmsweb.cern.ch/dqm/offline/jsonfairy/archive/321012/StreamExpress/Run2018D-Express-v1/DQMIO/Tracking/TrackParameters/generalTracks/GeneralProperties/TrackEtaPhi_ImpactPoint_GenTk"
response = cernrequests.get(url)
```

## FAQ

### How do i specify custom user certificate paths?

The default user certificate paths are ```~\private\usercert.pem``` and ```~\private\userkey.pem```. 

If you want to use different paths you can pass them to the cert argument:

```python
import cernrequests

url = "https://some.cern.ch/website"
cert = "my/custom/path/cert.pem"
key = "my/custom/path/key.pem"

cernrequests.get(url, cert=(cert,key))
```

## References

- http://docs.python-requests.org/en/master/
- https://certifi.io/en/latest/
- https://linux.web.cern.ch/linux/docs/cernssocookie.shtml
- http://linuxsoft.cern.ch/cern/centos/7/cern/x86_64/repoview/CERN-CA-certs.html
- https://ca.cern.ch/ca/