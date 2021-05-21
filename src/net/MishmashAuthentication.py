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

class MishmashClientMissingConfigurationVariableException(Exception):
    pass


class MishmashAuthentication():

    @staticmethod
    def get_authenticator(authentication_type):
        
        if authentication_type == "jwt":
            import mishmash_io_auth_jwt as auth_module
            return auth_module.MishmashAuth()

        elif authentication_type == 'azure':
            import mishmash_io_auth_azure as auth_module
            return auth_module.MishmashAuth()

        elif authentication_type == 'aws':
            import mishmash_io_auth_aws as auth_module
            return auth_module.MishmashAuth()

        elif authentication_type == 'google':
            import mishmash_io_auth_google as auth_module
            return auth_module.MishmashAuth()

        else:
            raise MishmashClientMissingConfigurationVariableException

        