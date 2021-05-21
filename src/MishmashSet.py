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

from MishmashLiteral import MishmashLiteral
from MishmashFunction import MishmashFunction
from MishmashExceptions import MishmashNotImplementedYetException
from utils import isinstance_datetime, isinstance_of_sequence


class MishmashSetSerializationUnsupportedTypeException(Exception):
    pass


class MishmashSetIntersectionWithUnknownException(Exception):
    pass


class MishmashSetUnionWithUnknownException(Exception):
    pass


class MishmashSetWrongKeyException(Exception):
    pass


class MishmashSet():
    """
        A representation of a set. MishmashSets provide context for the operations 
        and messages on a Mishmash.

        When a mishmashSet is built by using intersections(the 'member access') and unions ('list args' functionalities)
        a 'tree-like' structure is created in 'def'. Children represent intersections (sub-sets), arrays represent 'unions'. 

    """

    SERIALIZATION_PARAMETER_NAME = 's'

    def __init__(self):
        self.__def = []

    def __len__(self):
        return len(self.__def)

    def __str__(self):
        return str(self.to_json())

    def __repr__(self):
        return '{}()'.format(self.__class__.__name__)

    def __bool__(self):
        return bool(self.__def)

    def get_def(self):
        """
            Returns:
                list: this MishmashSet __def 
        """
        if not self.__def:
            return []

        if len(self.__def) == 1:
            return self.__def[0]

        return self.__def

    def is_empty(self):
        """
            Returns:
                bool: True if this MishmashSet is not empty, False otherwise 
        """
        return self.__bool__()

    def subset(self):
        """
            Returns a new set which is an intersection of the current one,
            but still has not  been specified as what it contains. It creates a new 'level'
            on which next _set() will operate

            Returns:
                MishmashSet: intersected new MishmashSet
        """

        new_subset = MishmashSet()
        for element in self.__def:
            new_subset.__def.append(element)

        new_subset.__def.append([])

        return new_subset

    def __set(self, value):
        """
            Sets the last element in this MishmashSet to the specified value.

            Parameters
            ----------
            value:
                new value which we want to add as last element in this MishmashSet

        """

        if len(self) == 0:
            self.__def.append(value)
        else:
            self.__def[-1] = value

        return self

    def __add(self, value):
        """
            Appends the specified value to the last element in this MishmashSet


            If the last element is an array, then simply append the specified value.

            If the last element is a value, then both it and the specified value are 
            added to an array, which replaces the last element

            __add is used to add one new element to the current 'level' (or node of the 'tree')

            Parameters
            ----------
            value:
                new value which we want to append to this MishmashSet

        """

        if len(self) == 0:
            self.__def.append(value)
        else:
            last = self.__def[-1]

            if isinstance(last, list):
                if len(last) == 0:
                    self.__set(value)
                else:
                    self.__def[-1].append(value)
            else:
                self.__set([last, value])

        return self

    def __intersect_null(self, v):
        return self.subset().__set(MishmashLiteral.null())

    def __intersect_boolean(self, v):
        return self.subset().__set(MishmashLiteral.boolean(v))

    def __intersect_integer(self, v):
        return self.subset().__set(MishmashLiteral.integer(v))

    def __intersect_float(self, v):
        return self.subset().__set(MishmashLiteral.double(v))

    def __intersect_string(self, v):
        return self.subset().__set(MishmashLiteral.string(v))

    def __intersect_sequence(self, v):

        new_subset = self

        for sequence_element in v:
            new_subset = new_subset.intersection(sequence_element)

        return self.intersection(new_subset)

    def __intersect_range(self, v):
        raise MishmashNotImplementedYetException("intersection with range")

    def __intersect_key_value_object(self, v):

        new_subset = self
        for key, value in v.items():

            key_value_element = MishmashSet()
            key_value_element = key_value_element.intersection(key)
            key_value_element = key_value_element.intersection(value)

            new_subset = new_subset.intersection(key_value_element)

        return self.intersection(new_subset)

    def __intersect_slice(self, v):
        raise MishmashNotImplementedYetException("intersection with slice")

    def __intersect_mishmash_object_set(self, arg):
        return self.subset().__set(arg)

    def __intersect_function(self, arg):
        return self.subset().__set(MishmashFunction(arg))

    def __intersect_datetime(self, v):
        return self.subset().__set(MishmashLiteral.datetime(v))

    def __intersect_bytes(self, v):
        raise MishmashNotImplementedYetException("intersect with bytes")

    def __intersect_bytearray(self, v):
        raise MishmashNotImplementedYetException("intersect with bytearray")

    def __intersect_memoryview(self, v):
        raise MishmashNotImplementedYetException("intersect with memoryview")

    def __intersect_namedtuple(self, v):
        raise MishmashNotImplementedYetException("intersect with namedtuple")

    def __intersect_generator(self, v):
        raise MishmashNotImplementedYetException("intersect with generator")

    def __intersect_method(self, v):
        raise MishmashNotImplementedYetException("intersect with method")

    def __intersect_lambda(self, v):
        raise MishmashNotImplementedYetException("intersect with lambda")

    def __intersect_unknown(self, v):
        raise MishmashSetIntersectionWithUnknownException(
            "cannot intersect with type {}".format(type(v)))

    def __union_null(self, v):
        return self.__add(MishmashLiteral.null())

    def __union_boolean(self, v):
        return self.__add(MishmashLiteral.boolean(v))

    def __union_integer(self, v):
        return self.__add(MishmashLiteral.integer(v))

    def __union_float(self, v):
        return self.__add(MishmashLiteral.double(v))

    def __union_complex(self, v):
        raise MishmashNotImplementedYetException(
            "complex number are not implemented yet")

    def __union_string(self, v):
        return self.__add(MishmashLiteral.string(v))

    def __union_unknown(self, v):
        raise MishmashSetUnionWithUnknownException(
            "cannot union with type {}".format(type(v)))

    def __union_sequence(self, v):

        new_subset = self

        for sequence_element in v:
            new_subset.union(sequence_element)

        return new_subset

    def __union_key_value_object(self, v):

        new_subset = self

        for key, value in v.items():

            key_value_elment = MishmashSet()
            key_value_elment = key_value_elment.intersection(key)
            key_value_elment = key_value_elment.intersection(value)
            new_subset.union(key_value_elment)

        return new_subset

    def __union_mishmash_object_set(self, arg):
        return self.__add(arg)

    def __union_function(self, arg):
        return self.__add(MishmashFunction(arg))

    def __union_datetime(self, v):
        return self.__add(MishmashLiteral.datetime(v))

    def __union_namedtuple(self, v):
        raise MishmashNotImplementedYetException(
            "union with namedtuple are not implemented yet")

    def __union_range(self, v):
        raise MishmashNotImplementedYetException(
            "union with range are not implemented yet")

    def __union_slice(self, v):
        raise MishmashNotImplementedYetException(
            "union with slice are not implemented yet")

    def __union_bytearray(self, v):
        raise MishmashNotImplementedYetException(
            "union with bytearray object are not implemented yet")

    def __union_memoryview(self, v):
        raise MishmashNotImplementedYetException(
            "union with memoryview object are not implemented yet")

    def __union_lambda(self, v):
        raise MishmashNotImplementedYetException(
            "union with lambda function are not implemented yet")

    def __union_generator(self, v):
        raise MishmashNotImplementedYetException(
            "union with generator are not implemented yet")

    def __union_method(self, v):
        raise MishmashNotImplementedYetException(
            "union with method are not implemented yet")

    def __union_bytes(self, v):
        raise MishmashNotImplementedYetException(
            "union with bytes object are not implemented yet")

    def union(self, *args):
        """
            Returns the union of this MishmashSet with the function arguments.
            Arguments can be of any type,
            and any number of arguments can be supplied.
        """
        new_set = copy(self)
        for arg in args:

            if arg is None:
                new_set = new_set.__union_null(arg)

            elif isinstance(arg, bool):
                new_set = new_set.__union_boolean(arg)

            elif isinstance(arg, int):
                new_set = new_set.__union_integer(arg)

            elif isinstance(arg, float):
                new_set = new_set.__union_float(arg)

            elif isinstance(arg, complex):
                new_set = new_set.__union_complex(arg)

            elif isinstance(arg, str):
                if not arg:
                    continue
                new_set = new_set.__union_string(arg)

            elif isinstance(arg, bytes):
                new_set = new_set.__union_bytes(arg)

            elif isinstance(arg, bytearray):
                new_set = new_set.__union_bytearray(arg)

            elif isinstance(arg, memoryview):
                new_set = new_set.__union_memoryview(arg)

            elif isinstance_of_sequence(arg):
                new_set = new_set.__union_sequence(arg)

            elif isinstance(arg, range):
                new_set = new_set.__union_range(arg)

            elif isinstance(arg, dict):
                new_set = new_set.__union_key_value_object(arg)

            elif isinstance(arg, slice):
                new_set = new_set.__union_slice(arg)

            elif isinstance(arg, MishmashSet):
                new_set = new_set.__union_mishmash_object_set(arg)

            elif isinstance_datetime(arg):
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
        """
        Returns the intersection of this MishmashSet with the function arguments.
            Arguments can be of any type,
            and any number of arguments can be supplied.
        """
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

            elif isinstance_of_sequence(arg):
                new_set = new_set.__intersect_sequence(arg)

            elif isinstance(arg, range):
                new_set = new_set.__intersect_range(arg)

            elif isinstance(arg, dict):
                new_set = new_set.__intersect_key_value_object(arg)

            elif isinstance(arg, slice):
                new_set = new_set.__intersect_slice(arg)

            elif isinstance(arg, bytes):
                new_set = new_set.__intersect_bytes(arg)
            elif isinstance(arg, bytearray):
                new_set = new_set.__intersect_bytearray(arg)
            elif isinstance(arg, memoryview):
                new_set = new_set.__intersect_memoryview(arg)

            elif isinstance(arg, MishmashSet):
                new_set = new_set.__intersect_mishmash_object_set(arg)
            elif isinstance_datetime(arg):
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

    def to_dict(self):
        """
            Returns the content of this MishmashSet as a dict 
            preserving the MishmashSet relations

            Returns:
                dict
        """

        def populate_set_descriptors(target_set, descriptors):

            if isinstance(target_set, MishmashSet):
                descriptors.append({self.SERIALIZATION_PARAMETER_NAME: []})

                populate_set_descriptors(target_set.get_def(),
                                         descriptors[-1][self.SERIALIZATION_PARAMETER_NAME])

            elif isinstance(target_set, list):

                for i in target_set:
                    populate_set_descriptors(i, descriptors)

            elif isinstance(target_set, MishmashFunction):
                descriptors.append(target_set.to_dict())

            elif isinstance(target_set, MishmashLiteral):
                descriptors.append(target_set.to_dict())

            else:
                raise MishmashSetSerializationUnsupportedTypeException(f"target set - {target_set} \
                                                    has unsupported type {type(target_set)} for serarilization")

        descriptors = []
        populate_set_descriptors(self.get_def(), descriptors)

        return {self.SERIALIZATION_PARAMETER_NAME: descriptors}

    @classmethod
    def from_dict(cls, set_dict):
        """
            Helper classmethod to construct a MishmashSet from a dictionary 
            preserving the MishmashSet relations

            Parameters:
            ----------
            set_dict(dict):
                given dict from which to construct a MishmashSet

            Returns:
                MishmashSet
        """

        result_set = []

        if isinstance(set_dict, dict):

            key = list(set_dict.keys())[0]
            if key == cls.SERIALIZATION_PARAMETER_NAME:
                if not set_dict[cls.SERIALIZATION_PARAMETER_NAME]:
                    return MishmashSet()

                result_set = MishmashSet()
                result_set.__def.append(cls.from_dict(
                    set_dict[cls.SERIALIZATION_PARAMETER_NAME]))
            elif key == "u":
                result_set = MishmashLiteral.from_dict(set_dict)

        elif isinstance(set_dict, list):
            if len(set_dict) == 1:
                result_set = MishmashLiteral.from_dict(set_dict[0])

            else:
                for i in set_dict:
                    result_set.append(cls.from_dict(i))

        return result_set

    @classmethod
    def from_json(cls, json_str):
        """
            Helper classmethod to construct a MishmashSet from a json string
            preserving the MishmashSet relations

            Parameters:
            ----------
            json_str(str):
                given json string from which to construct a MishmashSet

            Returns:
                MishmashSet
        """

        return cls.from_dict(json.loads(json_str))

    def to_json(self):
        """
            Returns json representation of this MishmashSet

            Returns:
                json string representing this MishmashSet
        """
        return json.dumps(self.to_dict())
