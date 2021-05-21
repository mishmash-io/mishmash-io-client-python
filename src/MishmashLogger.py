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

import sys
import logging
from logging import Logger


class MishmashLogger(Logger):
    
    def __init__(self, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", *args, **kwargs):
        self.formatter = logging.Formatter(format)

        Logger.__init__(self, self.__class__.__name__, *args, **kwargs)

        self.addHandler(self.get_console_handler())

    def get_console_handler(self):
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(self.formatter)
        return console_handler
