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

class MishmashConnectionParameters():

    SECURE_CONNECTION = 'secure'
    INSECURE_CONNECTION = 'insecure'

    def __init__(self, parameters):

        self.connection_type = MishmashConnectionParameters.INSECURE_CONNECTION
        try:
            self.url = parameters["url"]
            self.port = parameters["port"]
        except Exception as e:
            raise Exception("missing url and port params")


    def get_url(self):
        return self.url

    def get_connection_type(self):
        return self.connection_type

    def is_secure(self):
        return self.connection_type == MishmashConnectionParameters.SECURE_CONNECTION
