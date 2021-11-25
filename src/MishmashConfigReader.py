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

from MishmashExceptions import MishmashInvalidConfigException, MishmashMissingConfigVariableException

class MishmashConfigReader():

    def __init__(self, file_paths, required_vars, not_required_vars=None):

        if not file_paths:
            raise MishmashMissingConfigVariableException("please set config file paths")

        if not isinstance(file_paths, list):
            file_paths = [file_paths]
        
        self.file_paths = file_paths
 

        if not required_vars:
            raise MishmashMissingConfigVariableException("please set required variables")
        
        self.required_vars = set(required_vars)
        
        self.not_required_vars = None
        if not_required_vars:
            self.not_required_vars = set(not_required_vars)

    @staticmethod
    def load_config(file_path):
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            pass
        except ValueError as e:
            raise MishmashInvalidConfigException(e)
            
        return None

    def from_file(self):

        for file in self.file_paths:
            config = MishmashConfigReader.load_config(file)

            if config is not None:
                return config

        return {}

    def from_env(self):
        vars = list(self.required_vars) 
       
        if self.not_required_vars:
            list(self.not_required_vars)
       
        return {name : os.environ.get(name, None) for name in vars if os.environ.get(name, None) is not None}

    def validate_config_dict(self, config_dict):
        if not config_dict:
            raise MishmashMissingConfigVariableException(f"please set {', '.join(self.required_vars)} vars as config")

        missing = self.required_vars.difference(config_dict)
        if missing:
            raise MishmashMissingConfigVariableException(f"please set {', '.join(missing)} vars as config")
        
        return config_dict

    def get_configuration(self):
        config = self.from_file()
        env_config = self.from_env()

        if env_config:
            config.update(env_config)

        return  self.validate_config_dict(config)
