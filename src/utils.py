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

RECV_TIMEOUT = 2

def isinstance_datetime(arg):
    # todo add other date time types
    if isinstance(arg, datetime.datetime):
        return True
    elif isinstance(arg, datetime.date):
        return True
    else:
        return False
def str_to_bool(str_val):
    if isinstance(str_val, bool):
        return str_val

    if str_val == "true" or str_val == "True":
        return True
    elif str_val == "false" or str_val == "False":
        return False