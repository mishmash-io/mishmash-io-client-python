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

import datetime
import json
from typing import Iterable

RECV_TIMEOUT = 5  #value in seconds

class InvalidBooleanValueException(Exception):
    pass

class MissingConfigurationVariableException(Exception):
    pass


def isinstance_datetime(arg):

    if isinstance(arg, datetime.datetime):
        return True
    elif isinstance(arg, datetime.date):
        return True
    else:
        return False

def str_to_bool(str_val):
    
    if isinstance(str_val, bool):
        return str_val
    
    if isinstance(str_val, str):
        str_val = str_val.lower().capitalize()
    
    try:
        return eval(str_val)
    except Exception as e:
        pass

    return str_val

def value_or_exception(value):
    
    if value:
        return value
    
    raise MissingConfigurationVariableException()

def str_to_bool(str_val):
    
    if isinstance(str_val, bool):
        return str_val

    if isinstance(str_val, str):
        str_val = str_val.lower().capitalize()

        if str_val == "True":
            return True
        elif str_val == "False":
            return False
        else:
            raise InvalidBooleanValueException() from None

def is_jsonable(obj):
    
    try:
        json.dumps(obj)
        return True
    except (TypeError, OverflowError):
        return False

def is_class(obj):
    return isinstance(obj, type)

def is_iterable(obj):
    return isinstance(obj, Iterable)


def isinstance_of_sequence(arg):
    
    return isinstance(arg, list) or \
           isinstance(arg, tuple) or \
           isinstance(arg, set) or \
           isinstance(arg, frozenset)