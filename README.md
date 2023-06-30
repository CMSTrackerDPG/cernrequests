[![Build Status](https://travis-ci.com/CMSTrackerDPG/cernrequests.svg?branch=master)](https://travis-ci.com/CMSTrackerDPG/cernrequests)
[![](https://img.shields.io/pypi/v/cernrequests.svg)](https://pypi.org/project/cernrequests/)


# CERN Requests


Enables using [`requests`]("https://github.com/requests/requests") without having to configure the CERN Root certificates or getting an API access token manually.

Inspired by [`certifi`](https://github.com/certifi/python-certifi), [`requests-kerberos`](https://github.com/requests/requests-kerberos), [`cern-sso-python`](https://github.com/cerndb/cern-sso-python) and [`api-access-examples`](https://gitlab.cern.ch/authzsvc/docs/api-access-examples/-/tree/master/python).

The Root certificate bundle is copied from the [linuxsoft cern page](http://linuxsoft.cern.ch/cern/centos/7/cern/x86_64/repoview/CERN-CA-certs.html) and can also be created manually by downloading the CERN Grid Certification Authority files from [cafiles.cern.ch/cafiles](https://cafiles.cern.ch/cafiles/).

## Installation

Requires ```Python 2.7``` or ```Python 3.4+```

```bash
pip install cernrequests
```

## Prerequisites

### For sites requiring an SSL Grid certificate

Request a [Grid User Certificate](https://ca.cern.ch/ca/) (with password) and convert into public and private key:

```bash
mkdir -p ~/private
openssl pkcs12 -in myCertificate.p12 -clcerts -nokeys -out ~/private/usercert.pem  # Will ask for the certificate password
openssl pkcs12 -in myCertificate.p12 -nocerts -nodes -out ~/private/userkey.pem  # Will ask for the certificate password
```

The `.pem` certificates have to be **passwordless**.

### For CERN APIs using the ""new"" SSO

An `.env` file at the root of your project with the following variables set:
- `SSO_CLIENT_ID`
- `SSO_CLIENT_SECRET`

(You can rename the `.env_sample` file to `.env` and add the values there).

To request them, you will need to register your application:

1. Create an SSO registration for your application
    on the [CERN Application Portal](https://application-portal.web.cern.ch):

    ![](doc/create_registration_01.png)

2. Add an application identifier and description:

    ![](doc/create_registration_02.png)

    The `Application Identifier` can be anything, it's like a username for your application.t 
    
    Click `Submit`.

3. Go back to the Application Portal and edit the SSO application (green button). Then, go to the `SSO Registration` tab and click the plus button:

    ![](doc/create_registration_03.png)

4. Fill out the form of the new SSO registration as follows:

    ![](doc/create_registration_04.png)

    - You can put any value in the `Redirect URI(s)`, e.g. `http://localhost/*`
    - Same for the `Base URL`
    - Make sure you click `My application will need to get tokens using its own client ID and secret`.

5. Submit the form:

    ![](doc/create_registration_05.png)

    Note the `client id` and `client secret` that the form will show you.

## Usage

### Example

#### With Grid Certificates
```python
import cernrequests

url = "https://<your-cern-website>"
response = cernrequests.get(url)
```

#### With API Token

If you want to access a website which requires a (""new"") CERN Single Sign-on token you can do the following:

```python
import cernrequests

url = "https://<your-cern-website-url>"
reponse = cernrequests.get_with_token(url, target_audience="<the SSO id of the target URL>")
```
> **Note**
> The `target_audience` depends on the SSO registration name of the _target_ application. E.g.
> if you want to access the development instance of Run Registry, `target_audience` should be 
> `dev-cmsrunregistry-sso-proxy`. 
> In case of doubt, communicate with the app's developers directly. 

#### Alternative usage

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

### Grid certificates

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

The `cernrequests/cern-cacerts.pem` file has expired, and will need to be updated by the library maintainer. 

1. ```bash
    git clone https://gitlab.cern.ch/linuxsupport/rpms/cern-ca-certs/
    cd cern-ca-certs/src
    make
    ```
    This will create a `CERN-bundle.pem` file.
2. Rename it to `cern-cacerts.pem` and replace the original `.pem` certificate chain.

Verify that the certs work by running `pytest`.


### I'm getting `403 Client Error: Forbidden for url: https://login.cern.ch/adfs/ls/auth/sslclient` errors!1 What should I do?

1. Your grid certificate may have expired. Try creating a new one.
2. You may be trying to access a CERN webpage using a grid certificate, but this method may be deprecated. Make sure that the web page allows SSL certificate authentication.

## References

- http://docs.python-requests.org/en/master/
- https://certifi.io/en/latest/
- https://github.com/cerndb/cern-sso-python
- https://linux.web.cern.ch/linux/docs/cernssocookie.shtml
- http://linuxsoft.cern.ch/cern/centos/7/cern/x86_64/repoview/CERN-CA-certs.html
- https://ca.cern.ch/ca/
- https://auth.docs.cern.ch