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

from utils import str_to_bool, value_or_exception, InvalidBooleanValueException, MissingConfigurationVariableException

class MishmashConnectionParameters():
    
    DEFAULT_SSL_PORT = 443
    DEFAULT_PORT = 80
    
    DEFAULT_CONFIG_FILE_PATHS = [

        "/etc/mishmashio/client.json",
        "/etc/mishmashio/client-python.json",
        "~/.mishmashio/client.json",
        "~/.mishmashio/client-python.json",
        "./client.json",
        "./client-python.json"
    ]

    def __init__(self, config_file_path=None):

        self.config_file_paths = []
        if isinstance(config_file_path, str):
            self.config_file_paths.append(config_file_path)

        self.config_file_paths += self.DEFAULT_CONFIG_FILE_PATHS

        self.__raw_connection_parameters = self.get_configuration()

        try:
            self.__auth_method = value_or_exception(self.__raw_connection_parameters["MISHMASHIO_AUTH_METHOD"])
            self.__auth_app_id = value_or_exception(self.__raw_connection_parameters["MISHMASHIO_APP_ID"])
            self.__server_addresses = self.parse_server_list(value_or_exception(self.__raw_connection_parameters["MISHMASHIO_SERVERS"]))
            self.__use_ssl = str_to_bool(self.__raw_connection_parameters["MISHMASHIO_USE_SSL"])

        except KeyError as e:
            raise MissingConfigurationVariableException(
                "{} config variable is missing".format(e)) from None
                
        except InvalidBooleanValueException as e:
            raise InvalidBooleanValueException(
                " MISHMASHIO_USE_SSL value must be True / False ".format(e)) from None
    
        
    def get_configuration(self):
        configuration = self.get_configuration_from_file()

        if not configuration:
            configuration = self.get_configuration_from_env()

        return configuration

    def get_configuration_from_file(self):
        configuration = None
        for file_path in self.config_file_paths:
            try:
                with open(file_path, "r") as f:
                    configuration = json.load(f)
                    break
            except FileNotFoundError:
                pass
        return configuration

    def get_configuration_from_env(self):
        config = {
                "MISHMASHIO_AUTH_METHOD": os.environ.get("MISHMASHIO_AUTH_METHOD",None),
                "MISHMASHIO_APP_ID": os.environ.get("MISHMASHIO_APP_ID",None),
                "MISHMASHIO_SERVERS": os.environ.get("MISHMASHIO_SERVERS",None),
                "MISHMASHIO_USE_SSL": os.environ.get("MISHMASHIO_USE_SSL",None),
            }

        for k, v in config.items():
            if v is None:
                return None

        return config
            

    def parse_server_list(self, server_list):

        server_addresses = []
        for server in server_list:
            url_and_port = server.split(":")
            try:
                url, port = url_and_port
            except ValueError:
                url = url_and_port[0]
                if self.get_use_ssl():
                    port = self.DEFAULT_SSL_PORT
                else:
                    port = self.DEFAULT_PORT
            
            server_addresses.append((url, port))

        return server_addresses

    def get_url(self):
        return self.__server_addresses[0][0]

    def get_auth_method(self):
        return self.__auth_method

    def get_auth_app_id(self):
        return self.__auth_app_id

    def get_port(self):
        return int(self.__server_addresses[0][1])

    def get_use_ssl(self):
        return self.__use_ssl
