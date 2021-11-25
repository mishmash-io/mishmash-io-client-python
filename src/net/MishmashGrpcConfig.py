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

from MishmashConfigReader import MishmashConfigReader

from MishmashExceptions import MishmashWrongCredentialsException, MishmashModuleNotFoundException

from utils import parse_server_list, str_to_bool, load_credential_from_file

class MishmashGrpcConfig():
    
    CONFIG_FILE_PATHS = [

            "/etc/mishmashio/client.json",
            "/etc/mishmashio/client-python.json",
            "~/.mishmashio/client.json",
            "~/.mishmashio/client-python.json",
            "./client.json",
            "./client-python.json"
        ]

    ENV_VARIABLE_NAMES = [
        "MISHMASHIO_AUTH_METHOD",
        "MISHMASHIO_SERVERS",
        "MISHMASHIO_USE_SSL"
    ]
    NOT_REQUIRED_VARIABLE_NAMES = [
        "MISHMASH_CERT_FILE_PATH"
    ]

    DEFAULT_SSL_PORT = 443
    DEFAULT_PORT = 80

    def __init__(self):
      
        mishmash_config_reader = MishmashConfigReader(MishmashGrpcConfig.CONFIG_FILE_PATHS,
                                                      MishmashGrpcConfig.ENV_VARIABLE_NAMES,
                                                      MishmashGrpcConfig.NOT_REQUIRED_VARIABLE_NAMES)
                                                      
        self.__raw_config = mishmash_config_reader.get_configuration()

        if not isinstance(self.__raw_config["MISHMASHIO_AUTH_METHOD"], str):
            raise MishmashWrongCredentialsException(f"please provide valid MISHMASHIO_AUTH_METHOD")
        
        self.__auth_method = self.__raw_config["MISHMASHIO_AUTH_METHOD"]
        self.__is_ssl = str_to_bool(self.__raw_config["MISHMASHIO_USE_SSL"])

        if self.__is_ssl:
            if "MISHMASH_CERT_FILE_PATH" not in self.__raw_config:
                raise  MishmashWrongCredentialsException(f"please provide valid MISHMASH_CERT_FILE_PATH")
            
            self.__trusted_certs = load_credential_from_file( self.__raw_config["MISHMASH_CERT_FILE_PATH"])


        self.__server_address_list = parse_server_list(self.__raw_config["MISHMASHIO_SERVERS"], 
                                                    self.__is_ssl, 
                                                    MishmashGrpcConfig.DEFAULT_SSL_PORT, 
                                                    MishmashGrpcConfig.DEFAULT_PORT )

        self.__auth_plugin = self.__get_authenticaiton_plugin()

    def __get_authenticaiton_plugin(self):
        if self.__auth_method == "jwt":
            try:
                from mishmash_io_auth_jwt import MishmashAuth
            except ModuleNotFoundError:
                raise MishmashModuleNotFoundException("You have set MISHMASHIO_AUTH_METHOD to 'jwt'. . Please install mishmash_io_auth_jwt plugin")
            
            JWT_CONFIG_FILE_PATHS = [

                "/etc/mishmashio/client.json",
                "/etc/mishmashio/client-python.json",
                "~/.mishmashio/client.json",
                "~/.mishmashio/client-python.json",
                "./client.json",
                "./client-python.json"
            ]

            JWT_ENV_VARIABLE_NAMES = ["MISHMASHIO_APP_ID",
                                  "MISHMASHIO_AUTH_SERVER",
                                  "MISHMASHIO_AUTH_PRIVATE_KEY"]

            config_reader = MishmashConfigReader(JWT_CONFIG_FILE_PATHS, JWT_ENV_VARIABLE_NAMES)
            config_data = config_reader.get_configuration()

            return MishmashAuth(self.__server_address_list, config_data)
    
        elif self.__auth_method == "azure":
            try:
                from mishmash_io_auth_azure import MishmashAuth
            except ModuleNotFoundError:
                raise MishmashModuleNotFoundException("You have set MISHMASHIO_AUTH_METHOD to 'azure'. Please install mishmash_io_auth_jwt plugin")
            
            
            AZURE_CONFIG_FILE_PATHS = [
                "client.json"
            ]
            AZURE_ENV_VARIABLE_NAMES = ["AZURE_TENANT_ID",
                                "AZURE_CLIENT_ID",
                                "AZURE_THUMBPRINT",
                                "AZURE_PRIVATE_KEY_FILE_PATH",
                                "AZURE_API_SCOPES"]


            config_reader = MishmashConfigReader(AZURE_CONFIG_FILE_PATHS, AZURE_ENV_VARIABLE_NAMES)
            config_data = config_reader.get_configuration()
            return MishmashAuth(self.__server_address_list, config_data) 
        else:
            raise MishmashModuleNotFoundException("no auth plugin ")
    
    
    def get_server(self):
        return self.__server_address_list[0]

    def get_auth_method(self):
        return self.__auth_method

    @property
    def is_ssl(self):
        return self.__is_ssl

    @property
    def server_address_list(self):
        return self.__server_address_list
    
    @property
    def authorization_header(self):
        return self.__auth_plugin.authorization_header
        
    @property
    def app_id(self):
        return self.__auth_plugin.app_id
    
    @property
    def trusted_certs(self):
        return self.__trusted_certs