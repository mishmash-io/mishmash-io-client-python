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

import os
import json

current_file_path = os.path.dirname(__file__)

class MishmashConnectionParameters():
    #TODO add different config paths as list
    #TODO chnage CONFIG_FILE_NAME
    #TODO add ssl cert connections
    #TODO add different order for takeing config file
    
    SECURE_CONNECTION = 'secure'
    INSECURE_CONNECTION = 'insecure'

    ADDON_NAME = "VLADTEST"
    # ADDON_NAME = "MISHMASHIO"
    
    CONFIG_FILE_NAME = "client.json"
    
    AUTH_METHOD_NAME = '{}_AUTH_METHOD'.format(ADDON_NAME)
    AUTH_APP_ID_NAME = '{}_AUTH_APP_ID'.format(ADDON_NAME)
    SERVERS_NAME = "{}_SERVERS".format(ADDON_NAME)
    USE_SSl_NAME = '{}_USE_SSL'.format(ADDON_NAME)
    CONNECTION_TYPE_NAME = "{}_CONNECTION_TYPE".format(ADDON_NAME)
    URL_NAME = '{}_URL'.format(ADDON_NAME)
    PORT_NAME = '{}_PORT'.format(ADDON_NAME)

    def __init__(self, parameters):
    
        try:
            self.config_data = self.parse_config_file(self.CONFIG_FILE_NAME)
            self.config_data[self.CONNECTION_TYPE_NAME] = self.INSECURE_CONNECTION
        except Exception as e:
            try:
                self.config_data = self.parse_environment_vars()
                self.config_data[self.CONNECTION_TYPE_NAME] = self.INSECURE_CONNECTION
            except Exception as e:
                raise Exception("missing config variables")

    def set_dummy_connection_params(self):
        # TODO remove me
        config_data = {}
        print("\n\n\n url ot ofline_token are missing!!!")
        config_data[self.AUTH_APP_ID_NAME] = "fake_token"
        config_data[self.AUTH_METHOD_NAME] = "oidc_offline"
        config_data[self.URL_NAME] = "test-01.mishmash.io"
    
        config_data[self.PORT_NAME] = 443
        config_data[self.USE_SSl_NAME] = True
        print("set fake one\n--------------------\n")
        return config_data


    def parse_environment_vars(self):
        # TODO refactor
        config_data = {}
        try:
            config_data[self.AUTH_METHOD_NAME] = os.environ[self.AUTH_METHOD_NAME]
            config_data[self.AUTH_APP_ID_NAME] = os.environ[self.AUTH_APP_ID_NAME]
            server = os.environ[self.SERVERS_NAME]
            config_data[self.URL_NAME] = server.split(":")[0]
            config_data[self.PORT_NAME] = int(server.split(":")[1])
            config_data[self.USE_SSl_NAME] = os.environ[self.USE_SSl_NAME]
        except KeyError as e:
            # TODO what to do here
            config_data = self.set_dummy_connection_params()
            print(e)

        return config_data

    def parse_config_file(self, path):
        # TODO refactor
        config_data = {}

        try:
            with open(os.path.join(current_file_path, path), 'r') as f:
                data = json.load(f)
                print(data, path)
                config_data[self.AUTH_METHOD_NAME] = data[self.AUTH_METHOD_NAME]
                config_data[self.AUTH_APP_ID_NAME] = data[self.AUTH_APP_ID_NAME]
                server = data[self.SERVERS_NAME]
                config_data[self.URL_NAME] = server.split(":")[0]
                config_data[self.PORT_NAME] = int(server.split(":")[1])
                config_data[self.USE_SSl_NAME] = data[self.USE_SSl_NAME]

        except OSError as e:
            # TODO what to do here
            print(e)
            print("no config file at {}".format(path))
            config_data = self.set_dummy_connection_params()
        
        return config_data
        
    def get_url(self):
        return self.config_data[self.URL_NAME]

    def get_auth_method(self):
        return self.config_data[self.AUTH_METHOD_NAME]

    def get_auth_app_id(self):
        return self.config_data[self.AUTH_APP_ID_NAME]

    def get_port(self):
        return self.config_data[self.PORT_NAME]

    def get_use_ssl(self):
        return self.config_data[self.USE_SSl_NAME]

    def has_ssl_certificates(self):
        return self.config_data[self.CONNECTION_TYPE_NAME] == self.SECURE_CONNECTION
