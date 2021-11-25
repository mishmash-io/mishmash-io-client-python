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
import asyncio

from MishmashSet import MishmashSet
from MishmashLogger import MishmashLogger

from MishmashExceptions import MishmashNotImplementedYetException 

from net.MishmashGrpcClient import MishmashGrpcClient
from net.MishmashStream import MishmashStream
from net.MishmashMutation import MishmashMutation

from utils import is_jsonable, is_class, is_iterable

__all__ = ["mishmash"]

ATTR = ["_set", "loop", "config",
        "is_async", "logger", "async_stream", "logger","__grpc_client"]


class Mishmash():

    '''
        Core Mishmash module. 
        Provides methods for basic Mishmash interactions
    '''

    def __init__(self, is_async=False, loop=None, logger=None):

        MishmashGrpcClient()

        self._set = MishmashSet()
        self.is_async = is_async

        if not loop:
            loop = asyncio.get_event_loop()

        self.loop = loop

        if not logger:
            logger = MishmashLogger()

        self.logger = logger

    def set_config(self, is_async=False, loop=None, logger=None):

        if is_async != self.is_async:
            self.is_async = is_async

        if loop:
            self.loop = loop

        if logger:
            self.logger = logger

        return self

    def __len__(self):

        mishmash_len = next(iter(self.__intersection("__len")))

        if isinstance(mishmash_len, int):
            return mishmash_len

        return 0

    def __bool__(self):
        return bool(self.__len__())

    def __eq__(self, other):

        if not isinstance(other, Mishmash):
            return False

        are_equal = next(iter(self.__intersection("__equal").__union(other)))

        if isinstance(are_equal, bool):
            return are_equal

        return False

    def __del__(self):
        pass

    def __iter__(self):
        return MishmashStream(self._set).sync_stream()

    def __next__(self):
        raise MishmashNotImplementedYetException("__next__ not implemented next")

    def __aiter__(self):
        return MishmashStream(self._set).async_stream()

    async def __anext__(self):
        raise MishmashNotImplementedYetException("__anext__ not implemented next")

    def __getattr__(self, name):

        if name in ATTR:
            return super().__getattribute__(name)

        return self.__getitem__(name)

    def __setattr__(self, name, value):

        if name in ATTR:
            super().__setattr__(name, value)
        else:
            self.__setitem__(name, value)

    def __getitem__(self, name):

        new_mishmash = self.__intersection(name)

        if self.is_async:
            raise MishmashNotImplementedYetException(
                "not implemented async __getitem__ logic")

        return new_mishmash

    def __setitem__(self, name, value):
        if is_iterable(name):
            base_set = self._set.intersection(
                self.transform_args_to_mishmash_set_values(*name))
        else:
            base_set = self._set.intersection(
                self.transform_args_to_mishmash_set_values(name))

        self._set = base_set
        self.__mutate(base_set, value)

    def __call__(self, *args, **kwargs):

        if not args and not kwargs:
            return self
        elif args and not kwargs:
            return self.__union(args)
        elif kwargs and not args:
            return self.__union(kwargs)
        else:
            return self.__union([*args, kwargs])

    def new_mishmash(self, new_set):
        '''
            return new 'child' Mishmash object, inheriting all settings of self
        '''
        res = self.__class__()
        res._set = new_set
        res.is_async = self.is_async
        res.loop = self.loop
        return res

    def __intersection(self, *args):
        '''
            Returns a new mishmash that represents the intersection of the supplied arguments.
        '''
        return self.new_mishmash(self._set.intersection(*self.transform_args_to_mishmash_set_values(*args)))

    def __union(self, *args):
        '''
            Returns a new mishmash that represents the union of the supplied arguments.
        '''
        return self.new_mishmash(self._set.subset().union(*self.transform_args_to_mishmash_set_values(*args)))

    def transform_args_to_mishmash_set_values(self, *args):
        '''
            Transform user arguments into MishmashSet values
        '''

        tranformed_arg = []
        for arg in args:

            if isinstance(arg, Mishmash):
                tranformed_arg.append(arg._set)

            elif is_class(arg):
                if is_jsonable(arg):
                    tranformed_arg.append(json.dumps(arg))
            else:
                tranformed_arg.append(arg)

        return tranformed_arg

    def __contains__(self, item):
        contains = next(iter(self.__intersection("__contains").__union(item)))

        result = next(iter(contains))
        if isinstance(result, bool):
            return result

        return False

    def __and__(self, other):
        return self.__intersection(other)

    def __or__(self, other):
        return self.__union(other)

    def __xor__(self, y):
        raise MishmashNotImplementedYetException(
            " xor logic not implemented yet")

    def __hash__(self):
        return id(self)

    def __mutate(self, base_set, values):
        if self.is_async:
            MishmashMutation().async_mutation(base_set, values)
        else:
            MishmashMutation().sync_mutation(base_set, values)


mishmash = Mishmash()
