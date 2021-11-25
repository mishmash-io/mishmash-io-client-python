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

from setuptools import setup

def readme():
    try:
        with open('README.md', 'r') as doc:
            return doc.read()
    except IOError:
        return """\
# mishmash-io-client

See [mishmash io](https://mishmash.io) for documentation.
"""

def version():
    with open('VERSION.txt', 'r') as version:
        return version.readline().strip()


setup(
    name='mishmash-io-client',
    version=version(),
    description='mishmash io client library',
    long_description=readme(),
    long_description_content_type='text/markdown',
    author='mishmash.io',
    author_email='info@mishmash.io',
    url='https://mishmash.io',
    project_urls={
        'Bug Tracker': 'https://github.com/mishmash-io/mishmash-io-client-python/issues',
        'Documentation': 'https://mishmash.io',
        'Source Code': 'https://github.com/mishmash-io/mishmash-io-client-python/',
    },
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
    python_requires='>=3.6, <4',

    package_dir = {'': 'src'},
    packages = ["", "net"],

    install_requires=[
        'mishmash-io-rpc>=0.0.5',
        'async-timeout'
    ],
    extras_require={
        'dev': [
            'pytest',
        ],
        'jwt': [
            'mishmash-io-auth-jwt>=0.0.2'
        ],
        'aws': [
            'mishmash-io-auth-aws>=0.0.2'
        ],
        'google': [
            'mishmash-io-auth-google>=0.0.2'
        ],
        'azure': [
            'mishmash-io-auth-azure>=0.0.2'
        ]
    }
)