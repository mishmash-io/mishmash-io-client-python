# Copyright 2019 MISHMASH I O OOD
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.build_py import build_py

import os
NAME = 'mishmash-io-client'
DESCRIPTION = 'mishmash io client library'
URL = 'https://mishmash.io'
EMAIL = 'info@mishmash.io'
AUTHOR = 'mishmash.io'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = '0.0.4'

def readme():
    try:
        with open('README.md', 'r') as doc:
            return doc.read()
    except IOError:
        return """\
# mishmash-io-client

See [mishmash io](https://mishmash.io) for documentation.
"""


with open('requirements.txt') as f:
    INSTALL_REQUIREMENTS = f.read().splitlines()

here = os.path.abspath(os.path.dirname(__file__))

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=readme(),
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    project_urls={
        'Bug Tracker': 'https://github.com/mishmash-io/mishmash-io-client-python/issues',
        'Documentation': 'https://mishmash.io',
        'Source Code': 'https://github.com/mishmash-io/mishmash-io-client-python/',
    },
    py_modules=[NAME],
    install_requires=INSTALL_REQUIREMENTS,
    extras_require={
        'dev': [
            'pytest',
        ]
    },
    setup_requires=[
        'wheel',
    ],
    include_package_data=True,
    license='Apache License v2.0',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Development Status :: 3 - Alpha',
        'Topic :: Database',
        'Topic :: Utilities',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries'
    ],
    keywords='database, artificial intelligence, development',

    package_dir = {'': 'src'},
    packages = ["", "net"]
)