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

from copy import copy
import json
import types
from datetime import datetime
import collections

from MishmashLiteral import MishmashLiteral
from MishmashFunction import MishmashFunction
from MishmashExceptions import MishmashNotImplementedYetException
import utils
import Mishmash


class MishmashSetIntersectionWithUnknownException(Exception):
    pass


class MishmashSetUnionWithUnknownException(Exception):
    pass


class MishmashSetWrongKeyException(Exception):
    pass


class MishmashSet():
    # TODO refactor set using copy / deep copy think for other alternative because deepcopy is very slow
    # TODO add other 'magic' methods? https://rszalski.github.io/magicmethods/
    # TODO add function and mishmash set to to/from dict

    SERIALIZATION_PARAMETER_NAME = 's'

    def __init__(self):
        self.__def = []

    def __len__(self):
        return len(self.__def)

    def __str__(self):
        return str(self.__def)

    def __repr__(self):
        # TODO think for different repr
        return str(self.__def)

    def __bool__(self):
        return bool(self.__def)

    def set_def(self, _def):
        self.__def = _def

    def get_def(self):

        if self.__def:
            if len(self.__def) == 1:
                return self.__def[0]
            else:
                return self.__def
        else:
            return []

    def is_empty(self):
        # TODO should i use magic method instead
        return not self.__def

    def subset(self):
        # // return a new set which is an intersection of the current one,
        #  but still has not  been specified as what it contains
        new_subset = MishmashSet()
        for d in self.__def:
            new_subset.__def.append(d)
        new_subset.__def.append([])
        return new_subset

    def union(self, *args):
        # TODO see if there is a problem with nested mishmash objects - use deep copy instead

        new_set = copy(self)
        for arg in args:

            if isinstance(arg, bool):
                new_set = new_set.__union_boolean(arg)
            elif isinstance(arg, int):
                new_set = new_set.__union_integer(arg)
            elif isinstance(arg, float):
                new_set = new_set.__union_float(arg)
            elif isinstance(arg, str):
                if not arg:
                    continue

                new_set = new_set.__union_string(arg)
            elif arg is None:
                new_set = new_set.__union_null(arg)
            elif isinstance(arg, list):
                new_set = new_set.__union_list(arg)
            elif isinstance(arg, tuple):
                # if isinstance(arg.__dict__, collections.abc.Mapping):
                #     new_set = new_set.__union_namedtuple(arg)
                # else:
                new_set = new_set.__union_tuple(arg)
            elif isinstance(arg, set):
                new_set = new_set.__union_set(arg)
            elif isinstance(arg, frozenset):
                new_set = new_set.__union_frozenset(arg)
            elif isinstance(arg, dict):
                new_set = new_set.__union_dict(arg)
            elif isinstance(arg, Mishmash.Mishmash) or isinstance(arg, MishmashSet):
                new_set = new_set.__union_mishmash_object(arg)
            elif isinstance(arg, range):
                new_set = new_set.__union_range(arg)
            elif isinstance(arg, slice):
                new_set = new_set.__union_slice(arg)
            elif isinstance(arg, bytes):
                new_set = new_set.__union_bytes(arg)
            elif isinstance(arg, bytearray):
                new_set = new_set.__union_bytearray(arg)
            elif isinstance(arg, memoryview):
                new_set = new_set.__union_memoryview(arg)
            elif utils.isinstance_datetime(arg):
                new_set = new_set.__union_datetime(arg)
            elif isinstance(arg, types.FunctionType):
                new_set = new_set.__union_function(arg)
            elif isinstance(arg, types.LambdaType):
                new_set = new_set.__union_lambda(arg)
            elif isinstance(arg, types.GeneratorType):
                new_set = new_set.__union_generator(arg)
            elif isinstance(arg, types.MethodType):
                new_set = new_set.__union_method(arg)
            else:
                new_set = new_set.__union_unknown(arg)

        return new_set

    def intersection(self, *args):
        # TODO see if there is a problem with nested mishmash objects - use deep copy instead
        new_set = copy(self)
        for arg in args:

            if isinstance(arg, bool):
                new_set = new_set.__intersect_boolean(arg)
            elif isinstance(arg, int):
                new_set = new_set.__intersect_integer(arg)
            elif isinstance(arg, float):
                new_set = new_set.__intersect_float(arg)
            elif isinstance(arg, str):
                if not arg:
                    continue
                new_set = new_set.__intersect_string(arg)
            elif arg is None:
                new_set = new_set.__intersect_null(arg)
            elif isinstance(arg, list):
                new_set = new_set.__intersect_list(arg)
            elif isinstance(arg, tuple):
                # if isinstance(arg.__dict__, collections.abc.Mapping):
                #     new_set = new_set.__intersect_namedtuple(arg)
                # else:
                new_set = new_set.__intersect_tuple(arg)
            elif isinstance(arg, set):
                new_set = new_set.__intersect_set(arg)
            elif isinstance(arg, frozenset):
                new_set = new_set.__intersect_frozenset(arg)
            elif isinstance(arg, dict):
                new_set = new_set.__intersect_dict(arg)
            elif isinstance(arg, range):
                new_set = new_set.__intersect_range(arg)
            elif isinstance(arg, slice):
                new_set = new_set.__intersect_slice(arg)

            elif isinstance(arg, bytes):
                new_set = new_set.__intersect_bytes(arg)
            elif isinstance(arg, bytearray):
                new_set = new_set.__intersect_bytearray(arg)
            elif isinstance(arg, memoryview):
                new_set = new_set.__intersect_memoryview(arg)
            # TODO is it ok to have
            elif isinstance(arg, Mishmash.Mishmash) or isinstance(arg, MishmashSet):
                new_set = new_set.__intersect_mishmash_object(arg)
            elif utils.isinstance_datetime(arg):
                new_set = new_set.__intersect_datetime(arg)
            elif isinstance(arg, types.FunctionType):
                new_set = new_set.__intersect_function(arg)
            elif isinstance(arg, types.LambdaType):
                new_set = new_set.__intersect_lambda(arg)
            elif isinstance(arg, types.GeneratorType):
                new_set = new_set.__intersect_generator(arg)
            elif isinstance(arg, types.MethodType):
                new_set = new_set.__intersect_method(arg)
            else:
                new_set = new_set.__intersect_unknown(arg)

        return new_set

    def __set(self, value):
        # Sets the last element in this set to the specified value.
        if len(self) == 0:
            self.__def.append(value)
        else:
            self.__def[-1] = value

        return self

    def __add(self, value):
        # Appends the specified value to the last element in this set
        #  If the last element is an array, then simply append the specified value.
        #  If the last element is a scalar value, then both it and the specified
        # value are added to an array, which replaces the last element.

        if len(self) == 0:
            self.__def.append(value)
        else:
            last = self.__def[-1]

            if isinstance(last, list):
                if len(last) == 0:
                    self.__set(value)
                else:
                    last.append(value)
                    self.__def[-1] = last
            else:
                self.__set([last, value])

        return self

    def __intersect_boolean(self, v):
        return self.subset().__set(MishmashLiteral.boolean(v))

    def __intersect_integer(self, v):
        return self.subset().__set(MishmashLiteral.integer(v))

    def __intersect_double(self, v):
        return self.subset().__set(MishmashLiteral.double(v))

    def __intersect_string(self, v):
        return self.subset().__set(MishmashLiteral.string(v))

    def __intersect_null(self, v):
        return self.subset().__set(MishmashLiteral.null())

    def __intersect_sequence(self, v):
        new_subset = MishmashSet()
        for i in v:
            new_subset = new_subset.intersection(i)

        return self.intersection(new_subset)

    def __intersect_key_value_object(self, v):

        dict_set = MishmashSet()
        for k, v in v.items():
            dict_elm = MishmashSet()
            dict_elm = dict_elm.intersection(k)
            dict_elm = dict_elm.intersection(v)
            dict_set = dict_set.intersection(dict_elm)

        return self.intersection(dict_set)

    def __intersect_list(self, v):
        return self.__intersect_sequence(v)

    def __intersect_tuple(self, v):
        return self.__intersect_sequence(v)

    def __intersect_set(self, v):
        return self.__intersect_sequence(v)

    def __intersect_frozenset(self, v):
        return self.__intersect_sequence(v)

    def __intersect_range(self, v):
        raise MishmashNotImplementedYetException("intersection with range")

    def __intersect_slice(self, v):
        raise MishmashNotImplementedYetException("intersection with slice")

    def __intersect_dict(self, v):
        return self.__intersect_key_value_object(v)

    def __intersect_mishmash_object(self, arg):
        return self.subset().__set(arg)

    def __intersect_function(self, arg):
        return self.subset().__set(MishmashFunction(arg))

    def __intersect_datetime(self, v):
        return self.subset().__set(MishmashLiteral.datetime(v))

    def __intersect_byte(self, v):
        raise MishmashNotImplementedYetException("intersect with byte")

    def __intersect_bytearray(self, v):
        raise MishmashNotImplementedYetException("intersect with bytearray")

    def __intersect_memoryview(self, v):
        raise MishmashNotImplementedYetException("intersect with memoryview")

    def __intersect_namedtuple(self, v):
        return self.__intersect_key_value_object(v)

    def __intersect_generator(self, v):
        raise MishmashNotImplementedYetException("intersect with generator")

    def __intersect_method(self, v):
        raise MishmashNotImplementedYetException("intersect with method")

    def __intersect_lambda(self, v):
        raise MishmashNotImplementedYetException("intersect with lambda")

    def __intersect_unknown(self, v):
        raise MishmashSetIntersectionWithUnknownException(
            "cannot intersect with type {}".format(type(v)))

    def __union_boolean(self, v):
        return self.__add(MishmashLiteral.boolean(v))

    def __union_integer(self, v):
        return self.__add(MishmashLiteral.integer(v))

    def __union_float(self, v):
        return self.__add(MishmashLiteral.double(v))

    def __union_string(self, v):
        return self.__add(MishmashLiteral.string(v))

    def __union_null(self, v):
        return self.__add(MishmashLiteral.null())

    def __union_unknown(self, v):
        raise MishmashSetUnionWithUnknownException(
            "cannot union with type {}".format(type(v)))

    def __union_sequence(self, v):

        new_set = MishmashSet()
        for arg in v:
            new_set.union(arg)

        return self.union(new_set)

    def __union_key_value_object(self, arg):
        dict_set = MishmashSet()

        for k, v in arg.items():
            dict_elm = MishmashSet()
            dict_elm = dict_elm.intersection(k)
            dict_elm = dict_elm.intersection(v)
            dict_set.union(dict_elm)

        return self.union(dict_set)

    def __union_list(self, v):
        return self.__union_sequence(v)

    def __union_set(self, v):
        return self.__union_sequence(v)

    def __union_frozenset(self, v):
        return self.__union_sequence(v)

    def __union_tuple(self, v):
        return self.__union_sequence(v)

    def __union_dict(self, arg):
        return self.__union_key_value_object(arg)

    def __union_mishmash_object(self, arg):
        return self.__add(arg)

    def __union_function(self, arg):
        return self.__add(MishmashFunction(arg))
    #    return isinstance(x, types.FunctionType) \
    #     or isinstance(x, types.BuiltinFunctionType)

    def __union_datetime(self, v):
        return self.__add(MishmashLiteral.datetime(v))

    def __union_namedtuple(self, v):
        raise MishmashNotImplementedYetException("union with namedtuple")

    def __union_range(self, v):
        raise MishmashNotImplementedYetException("union with range")

    def __union_slice(self, v):
        raise MishmashNotImplementedYetException("union with slice")

    def __union_byte(self, v):
        raise MishmashNotImplementedYetException("union with byte")

    def __union_bytearray(self, v):
        raise MishmashNotImplementedYetException("union with bytearray")

    def __union_memoryview(self, v):
        raise MishmashNotImplementedYetException("union with memoryview")

    def __union_lambda(self, v):
        raise MishmashNotImplementedYetException("union with lambda")

    def __union_generator(self, v):
        raise MishmashNotImplementedYetException("union with generator")

    def __union_method(self, v):
        raise MishmashNotImplementedYetException("union with method")

    def to_dict(self):

        def populate_set_descriptors(target_set, descriptors):

            if isinstance(target_set, MishmashSet):

                descriptors.append({self.SERIALIZATION_PARAMETER_NAME: []})
                populate_set_descriptors(target_set.get_def(
                ), descriptors[-1][self.SERIALIZATION_PARAMETER_NAME])

            elif isinstance(target_set, list):

                for v in target_set:
                    populate_set_descriptors(v, descriptors)

            elif isinstance(target_set, MishmashFunction):
                descriptors.append(target_set.to_dict())
            elif isinstance(target_set, MishmashLiteral):
                descriptors.append(target_set.to_dict())
            else:
                raise Exception(
                    "wrong type passed to descriptor list", type(target_set))

        descriptors = []
        populate_set_descriptors(self.get_def(), descriptors)

        return {self.SERIALIZATION_PARAMETER_NAME: descriptors}

    @classmethod
    def from_dict(cls, dict_set):
        result_set = []

        if isinstance(dict_set, dict):
            # TODO add other types as functions etc
            key = list(dict_set.keys())[0]
            if key == cls.SERIALIZATION_PARAMETER_NAME:
                if not dict_set[cls.SERIALIZATION_PARAMETER_NAME]:
                    return MishmashSet()

                result_set = MishmashSet()
                result_set.__def.append(cls.from_dict(
                    dict_set[cls.SERIALIZATION_PARAMETER_NAME]))
            elif key == "u":
                result_set = MishmashLiteral.from_dict(dict_set)
        elif isinstance(dict_set, list):
            if len(dict_set) == 1:
                result_set = MishmashLiteral.from_dict(dict_set[0])

            else:
                for i in dict_set:
                    result_set.append(cls.from_dict(i))

        return result_set

    @classmethod
    def fromJson(cls, json_str):
        tmp = json.loads(json_str)
        return cls.from_dict(tmp)

    def toJson(self):
        return json.dumps(self.to_dict())
