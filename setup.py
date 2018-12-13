from setuptools import setup

setup(
    name="cernrequests",
    version="0.1",
    desription="CERN wrapper around the requests package",
    url="https://github.com/ptrstn/cernrequests",
    author="Peter Stein",
    author_email="peter.stein@cern.ch",
    packages=['cernrequests'],
    package_dir={'cernrequests': 'cernrequests'},
    package_data={'cernrequests': ['*.pem']},
    install_requires=["requests", "future"],
)
