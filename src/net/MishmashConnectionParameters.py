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


class MishmashConnectionParameters():
    DEFAULT_SSL_PORT = 443
    DEFAULT_PORT = 80
    CONFIG_PATHS = [
        ("/etc/mishmashio", "client.json"),
        ("/etc/mishmashio", "client-python.json"),
        ("~/.mishmashio", "client.json"),
        ("~/.mishmashio", "client-python.json"),
        ("./", "client.json")
    ]

    def __init__(self):

        connection_parameters = self.get_configuration()

        try:
            self.__auth_method = connection_parameters["MISHMASHIO_AUTH_METHOD"]
            self.__auth_app_id = connection_parameters["MISHMASHIO_AUTH_APP_ID"]
            self.__servers = connection_parameters["MISHMASHIO_SERVERS"]
            self.__use_ssl = connection_parameters["MISHMASHIO_USE_SSL"]
            self.__raw_connection_parameters = connection_parameters

        except KeyError as e:
            raise Exception("missing config variable {}".format(e))

    def get_configuration(self):

        config = {}

        for path, name in self.CONFIG_PATHS:
            try:
                config = self.parse_config_file(path, name)
                break
            except FileNotFoundError:
                pass

        if not config:
            try:
                config = self.parse_env_vars()
            except:
                raise Exception("no valid configuration")

        return config

    def parse_env_vars(self):

        def get_var_with_exception(env_vars, name):
            v = env_vars.get(name, None)
            if not v:
                raise Exception("missing config variable {}".format(name))

            return v

        config = {
            "MISHMASHIO_AUTH_METHOD": get_var_with_exception(os.environ, "MISHMASHIO_AUTH_METHOD"),
            "MISHMASHIO_AUTH_APP_ID": get_var_with_exception(os.environ, "MISHMASHIO_AUTH_APP_ID"),
            "MISHMASHIO_SERVERS": get_var_with_exception(os.environ, "MISHMASHIO_SERVERS"),
            "MISHMASHIO_USE_SSL": get_var_with_exception(os.environ, "MISHMASHIO_USE_SSL"),
        }

        return config

    def parse_config_file(self, path, name):
        with open(os.path.join(path, name), "r") as config_file:
            return json.load(config_file)

    def parse_server(self, server):

        split = server.split(":")
        try:
            url, port = split
        except ValueError:
            url = split[0]
            if self.get_use_ssl():
                port = self.DEFAULT_SSL_PORT
            else:
                port = self.DEFAULT_PORT

        return url, port

    def get_url(self):
        # TODO use server list
        return self.parse_server(self.__servers)[0]

    def get_auth_method(self):
        return self.__auth_method

    def get_auth_app_id(self):
        return self.__auth_app_id

    def get_port(self):
        return int(self.parse_server(self.__servers)[1])

    def get_use_ssl(self):
        return self.__use_ssl


