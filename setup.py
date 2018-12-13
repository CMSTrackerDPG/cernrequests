from setuptools import setup, find_packages

setup(
    name="cernrequests",
    version="0.1",
    desription="CERN wrapper around the requests package",
    url="https://github.com/ptrstn/cernrequests",
    author="Peter Stein",
    author_email="peter.stein@cern.ch",
    packages=find_packages(),
    install_requires=["requests", "future"],
)
