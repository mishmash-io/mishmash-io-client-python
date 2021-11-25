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

import platform
import inspect

def handle_stackframe_without_leak():
    frame = inspect.currentframe()
    try:
        print(inspect.getframeinfo(frame))
    finally:
        del frame

class MishmashFunction():

    SERIALIZATION_PARAMETER_NAME = 'f'

    def __init__(self, function_object):
        self.function_object = function_object

        self.name = function_object.__name__
        self.body = inspect.getsource(function_object)
        self.client_runtime = "Python {}".format(platform.python_version())
        self.scope_id = "not implemented yet"
        self.clojure = inspect.signature(function_object)

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.body)

    def to_dict(self):
        
        serialized_json = {
            self.SERIALIZATION_PARAMETER_NAME: [self.name, self.body]
        }

        return serialized_json
