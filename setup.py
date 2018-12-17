from setuptools import setup

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="cernrequests",
    version="0.1",
    desription="CERN wrapper around the requests package",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/ptrstn/cernrequests",
    author="Peter Stein",
    author_email="peter.stein@cern.ch",
    packages=['cernrequests'],
    package_dir={'cernrequests': 'cernrequests'},
    package_data={'cernrequests': ['*.pem']},
    install_requires=["requests", "future"],
)
