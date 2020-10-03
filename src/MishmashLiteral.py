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

import json

from MishmashOp import MishmashOp


class MishmashLiteralDeserializeException(Exception):
    pass


class MishmashLiteral(object):
    # TODO do i need param set for op type
    # TODO add other 'magic' methods? https://rszalski.github.io/magicmethods/
    TYPE_OP = 'o'
    TYPE_UNKNOWN = "u"
    LITERAL_TYPES = [TYPE_OP, TYPE_UNKNOWN]

    def __init__(self, literal=None, literal_type=None):
        self.__def = {}
        self.__def["literal"] = literal
        self.__def["type"] = self.to_literal_type(literal_type)

    def __str__(self):
        return str(self.to_dict())

    def __repr__(self):
        return '{}({}, {})'.format(self.__class__.__name__, self.__def["literal"], self.__def["type"])

    def __eq__(self, other):
        if self.get_type() == other.get_type() and self.get_literal() == other.get_literal():
            return True
        else:
            return False

    def is_op(self):
        return self.__def['type'] == self.TYPE_OP

    def is_unknown(self):
        return self.__def['type'] == self.TYPE_UNKNOWN

    def get_type(self):
        return self.__def['type']

    def get_literal(self):
        return self.__def['literal']

    def to_literal_type(self, literal_type):
        if literal_type in MishmashLiteral.LITERAL_TYPES:
            return literal_type
        else:
            return MishmashLiteral.TYPE_UNKNOWN

    @classmethod
    def boolean(cls, value, literal_type=None):
        return cls(value, literal_type)

    @classmethod
    def integer(cls, value, literal_type=None):
        return cls(value, literal_type)

    @classmethod
    def double(cls, value, literal_type=None):
        return cls(value, literal_type)

    @classmethod
    def datetime(cls, value, literal_type=None):
        return cls(value, literal_type)

    @classmethod
    def string(cls, value, literal_type=None):
        op = MishmashOp.get_op_id(value)

        if op and literal_type is None:
            return cls(value, cls.TYPE_OP)

        return cls(value, literal_type)

    @classmethod
    def null(cls, literal_type=None):
        return cls(None, literal_type)

    def pretty_print(self):
        pretty_value = self.__def['literal']
        if isinstance(pretty_value, int):
            return '[{}]'.format(pretty_value)
        return "{}".format(pretty_value)

    def to_dict(self):
        serialized_json = {self.__def['type']: self.__def['literal']}
        return serialized_json

    @classmethod
    def from_dict(cls, _dict):
        literal = None
        literal_type = None
        for k, v in _dict.items():
            if k in cls.LITERAL_TYPES:
                literal = v
                literal_type = k
            else:
                raise MishmashLiteralDeserializeException(
                    "cannot deserialize literal with key ", k)

        return cls(literal, literal_type)

    @classmethod
    def from_json(cls, json_str):
        return cls.from_dict(json.loads(json_str))

    def to_json(self):
        return json.dumps(self.to_dict())
