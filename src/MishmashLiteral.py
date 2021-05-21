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
    """

        MishmashLiteral class represents the various
        literal types supported by the Mishmash.

        Parameters
        ----------
        literal:
            represent the value of the MishmashLiteral
        literal_type:
            specify literal type, if needed
    """

    TYPE_OP = 'o'
    TYPE_UNKNOWN = 'u'
    LITERAL_TYPES = [TYPE_OP, TYPE_UNKNOWN]

    def __init__(self, literal=None, literal_type=None):
        self.__def = {}
        self.__def["literal"] = literal
        self.__def["type"] = self.set_literal_type(literal_type)

    def __str__(self):
        return str(self.to_dict())

    def __repr__(self):
        return '{}({}, {})'.format(self.__class__.__name__, self.__def["literal"], self.__def["type"])

    def __eq__(self, other):

        if not isinstance(other, MishmashLiteral):
            return NotImplemented

        return self.get_type() == other.get_type() and \
            self.get_literal() == other.get_literal()

    def get_type(self):
        """
            Get type of this MishmashLiteral

            Returns:
                string: String representation of MishmashLiteral type
        """
        return self.__def['type']

    def get_literal(self):
        """
            Get value of this MishmashLiteral

            Returns:
                the value of this literal.
        """
        return self.__def['literal']

    @classmethod
    def set_literal_type(cls, literal_type):
        """
            Converts MishmashLiteral to new literal type 

            Parameters
            ----------
            literal_type:
                new type

            Returns:
                string: String representation of MishmashLiteral type
        """

        if literal_type in cls.LITERAL_TYPES:
            return literal_type

        return cls.TYPE_UNKNOWN

    def is_op(self):
        """
            Check if type of this MishmashLiteral is MishmashOp

            Returns:
                True(bool): if the literal type is a MishmashOp
        """
        return self.__def['type'] == self.TYPE_OP

    def is_unknown(self):
        """
            Check if type of this MishmashLiteral is unknown (not important for the user)

            Returns:
                True(bool): if the literal is a unknown
        """
        return self.__def['type'] == self.TYPE_UNKNOWN

    @classmethod
    def boolean(cls, value, literal_type=None):
        # TODO can value be different from boolean
        """
            Helper classmethod to construct a MishmashLiteral from a boolean literal

            Parameters:
            ----------
            value:
                new value

            Returns:
                MishmashLiteral
        """
        return cls(value, literal_type)

    @classmethod
    def integer(cls, value, literal_type=None):
        """
            Helper classmethod to construct a MishmashLiteral from a new integer literal

            Parameters:
            ----------
            value:
                new value

            Returns:
                MishmashLiteral
        """
        return cls(value, literal_type)

    @classmethod
    def double(cls, value, literal_type=None):
        """
            Helper classmethod to construct a MishmashLiteral from a double literal

            Parameters:
            ----------
            value:
                new value

            Returns:
                MishmashLiteral
        """
        return cls(value, literal_type)

    @classmethod
    def datetime(cls, value, literal_type=None):
        """
            Helper classmethod to construct a MishmashLiteral from a datetime literal

            Parameters:
            ----------
            value:
                new value

            Returns:
                MishmashLiteral
        """
        return cls(value, literal_type)

    @classmethod
    def string(cls, value, literal_type=None):
        """
            Helper classmethod to construct a MishmashLiteral from a string literal

            Parameters:
            ----------
            value:
                new value

            Returns:
                MishmashLiteral
        """
        op = MishmashOp.get_op_id(value)

        if op and literal_type is None:
            return cls(value, cls.TYPE_OP)

        return cls(value, literal_type)

    @classmethod
    def null(cls, literal_type=None):
        """
            Helper classmethod to construct a MishmashLiteral from a null literal

            Parameters:
            ----------
            value:
                new value

            Returns:
                MishmashLiteral
        """
        return cls(None, literal_type)

    @classmethod
    def from_dict(cls, literal_dict):
        """
            Helper classmethod to construct a MishmashLiteral from a dictionary 
            preserving the literal type- literal relations

            Parameters:
            ----------
            literal_dict(dict):
                given dict from which to construct a MishmashLiteral

            Returns:
                MishmashLiteral
        """

        if not isinstance(literal_dict, dict):
            raise MishmashLiteralDeserializeException(
                "cannot deserialize object {} of type {}".format(literal_dict, type(literal_dict)))

        literal_type, literal = next(iter(literal_dict.items()))

        if literal_type not in cls.LITERAL_TYPES:
            raise MishmashLiteralDeserializeException(
                "cannot deserialize literal of type ", literal_type)

        return cls(literal, literal_type)

    def to_dict(self):
        """
            Returns the contents of this MishmashLiteral as a dict with
            literal type as key and literal as value


            Returns:
                dict {literal_type:literal}
        """

        serialized_json = {self.__def['type']: self.__def['literal']}
        return serialized_json

    @classmethod
    def from_json(cls, json_str):
        """
            Helper classmethod to construct a MishmashLiteral from a json string
            preserving the literal_type- literal relations

            Parameters:
            ----------
            json_str(str):
                given json string from which to construct a MishmashLiteral

            Returns:
                new MishmashLiteral
        """

        return cls.from_dict(json.loads(json_str))

    def to_json(self):
        """
            Returns json representation of this MishmashLiteral

            Returns:
                string: json string representing this MishmashLiteral
        """

        return json.dumps(self.to_dict())

    def pretty_print(self):

        pretty_value = self.__def['literal']
        if isinstance(pretty_value, int):
            return '[{}]'.format(pretty_value)

        return "{}".format(pretty_value)
