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
from MishmashExceptions import MishmashNotImplementedYetException
from MishmashLogger import MishmashLogger

from net.ConnectionFactory import ConnectionFactory
from net.MishmashConnectionParameters import MishmashConnectionParameters
from net.MishmashStream import MishmashStream
from net.MishmashMutation import MishmashMutation

from utils import is_jsonable, is_class, is_iterable

__all__ = ["mishmash"]

ATTR = ["_set", "loop", "connection_parameters",
        "is_async", "logger", "async_stream", "logger"]


class Mishmash():

    '''
        Core Mishmash module. 
        Provides methods for basic Mishmash interactions
    '''

    def __init__(self, is_async=False, loop=None, logger=None):

        self._set = MishmashSet()
        self.is_async = is_async
        self.connection_parameters = MishmashConnectionParameters()
        self.loop = loop
        self.async_stream = None

        if not logger:
            logger = MishmashLogger()

        self.logger = logger

        ConnectionFactory.set_connection(self.connection_parameters)

    def set_config(self, loop=None, is_async=False):

        if is_async != self.is_async:
            self.is_async = is_async

        if loop:
            self.loop = loop

        return self

    def __len__(self):

        mishmash_len = next(iter(self.__intersection("__len")))

        if isinstance(mishmash_len, int):
            return mishmash_len

        return 0

    def __bool__(self):
        return self.__len__()

    def __eq__(self, other):

        if not isinstance(other, Mishmash):
            return False

        are_equals = self.__intersection("__equal").__union(other)

        result = next(iter(are_equals))

        if isinstance(result, bool):
            return result

        return False
    
    def __del__(self):
        ConnectionFactory.close_channel() 

    def __iter__(self):

        for i in self.__sync_download():
            yield i

    def __aiter__(self):

        stream = MishmashStream(self._set)
        self.async_stream = stream.run()

        return self

    async def __anext__(self):
        return await self.__async_download()

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

        if self.is_async:
            self.__async_upload(base_set, value)
        else:
            self.__sync_upload(base_set, value)

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
        res.connection_parameters = self.connection_parameters

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

    def __sync_download(self):
        stream = MishmashStream(self._set)
        stream_generator = stream.run()

        if not self.loop:
            self.loop = asyncio.get_event_loop()

        while True:
            try:
                res = stream_generator.__anext__()
                yield self.loop.run_until_complete(res)
            except StopAsyncIteration:
                break
            except asyncio.TimeoutError:
                break

    async def __async_download(self):

        next_elemnet = await self.async_stream.__anext__()
        try:
            return next_elemnet
        except StopAsyncIteration:
            self.async_stream = None
        except asyncio.TimeoutError:
            self.async_stream = None

    def __sync_upload(self, base_set, *values):
        if not self.loop:
            self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self.__async_upload(base_set, *values))

    async def __async_upload(self, base_set, *values):
        mutate = MishmashMutation(base_set, *values)
        mutate_generator = mutate.run()
        await mutate_generator

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

           
        
mishmash = Mishmash()
