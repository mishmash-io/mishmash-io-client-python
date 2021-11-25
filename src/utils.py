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

import json

from MishmashExceptions import MishmashWrongCredentialsException

MUTATION_TYPE_OVERWRITE ='overwrite'
MUTATION_TYPE_APPEND ='append'


class InvalidBooleanValueException(Exception):
    pass

def parse_server_list(server_list, use_ssl, DEFAULT_SSL_PORT, DEFAULT_PORT):
    """
        Returns  parsed list of ips and ports
    """
    if isinstance(server_list, str):
        try:
            server_list= json.loads(server_list)
        except json.decoder.JSONDecodeError:
            raise MishmashWrongCredentialsException("Please provide server list in json format as list of strings ['ip:port']")

    server_addresses = []
    for server in server_list:
        url_and_port = server.split(":")
        try:
            url, port = url_and_port
        except ValueError:
            url = url_and_port[0]
            if  use_ssl:
                port = DEFAULT_SSL_PORT
            else:
                port = DEFAULT_PORT
        
        server_addresses.append(f"{url}:{port}")

    return server_addresses

def str_to_bool(str_val):
    
    if isinstance(str_val, bool):
        return str_val

    if isinstance(str_val, str):
        str_val = str_val.lower()

        if str_val in ['true', 'yes', 'y']:
            return True
        elif str_val in ['false','no', 'n', '']:
            return False
        else:
            raise InvalidBooleanValueException() from None
      

from typing import Iterable


def is_jsonable(obj):
    
    try:
        json.dumps(obj)
        return True
    except (TypeError, OverflowError):
        return False

def is_class(obj):
    return isinstance(obj, type)

def is_iterable(obj):
    if isinstance(obj, str):
        return False
    return isinstance(obj, Iterable)
from datetime import datetime

def isinstance_datetime(arg):

    if isinstance(arg, datetime.datetime):
        return True
    elif isinstance(arg, datetime.date):
        return True
    else:
        return False


def isinstance_of_sequence(arg):
    
    return isinstance(arg, list) or \
           isinstance(arg, tuple) or \
           isinstance(arg, set) or \
           isinstance(arg, frozenset)


def load_credential_from_file(filepath):
    with open(filepath, 'rb') as f:
        return f.read()