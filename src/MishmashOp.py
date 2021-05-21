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


class MishmashOp(object):
    """
        MishmashOp class represents various predefined operations(op) 
        supported by the Mishmash.
    """
    OP_PREFIX = '__'
    OP_PREFIX_LEN = len(OP_PREFIX)

    OPS = {
        'avg': 'avg',
        'coalesce': 'coalesce',
        'filter': 'filter',
        'len': 'len',
        'equal':'equal',
        'contains':'contains'
    }

    @classmethod
    def get_op_id(cls, literal):
        """
            Finds the op id for the specified string

            Parameters
            ----------
                literal(string): predefined operation name which we want to get

            Returns:
                string: predefined operation id for the specified string (if it exists)
                or None otherwise
        """

        literal_prefix = literal[:cls.OP_PREFIX_LEN]
        op_id = literal[cls.OP_PREFIX_LEN:]

        if literal_prefix != cls.OP_PREFIX:
            return None

        if op_id not in cls.OPS:
            return None

        return op_id
