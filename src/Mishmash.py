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

import asyncio

from net.ConnectionFactory import ConnectionFactory
from net.MishmashConnectionParameters import MishmashConnectionParameters
from net.MishmashStream import MishmashStream
from net.MishmashMutation import MishmashMutation

from MishmashSet import MishmashSet
from MishmashExceptions import MishmashNoConfigException, MishmashNotImplementedYetException


ATTR = ["_set", "loop", "connection_parameters", "is_async"]


class Mishmash():

    # TODO logical operations over sets

    def __init__(self, config=None, is_async=False, loop=None):

        if config:
            self._set = MishmashSet()
            self.connection_parameters = MishmashConnectionParameters(config)
            self.is_async = is_async
            self.loop = loop
            ConnectionFactory.set_connection(self.connection_parameters)

    def __len__(self):
        return len(self._set)

    def __getitem__(self, name):
       
        new_mishmash = self.__intersection(name)

        if self.is_async:
            raise MishmashNotImplementedYetException("not implemented async logic")

        return new_mishmash

    def __eq__(self, s):
        raise MishmashNotImplementedYetException("not implemented async logic")

    def __setitem__(self, name, value):
        base_set = self._set

        if name:
            base_set = self._set.intersection(name)

        self.__upload(base_set, value)

    def __getattr__(self, name):

        
        if name in ATTR:
            return super().__getattribute__(name)

        return self.__getitem__(name)

    def __setattr__(self, name, value):
        # TODO think for  smarter way to avoid recursion
 
        if name in ATTR:
            super().__setattr__(name, value)
        else:
            self.__setitem__(name, value)

    def __call__(self, *args, **kwargs):

        if not args and not kwargs:
            return self
        elif args and not kwargs:
            return self.__union(*args)
        elif kwargs and not args:
            return self.__union(kwargs)
        else:
            return self.__union([*args, kwargs])

    def __iter__(self):
        for i in self.__download():
            yield i

    def new_mishmash(self, new_set):
        # // return new 'child' Mishmash object, inheriting all settings from $this
        # TODO more pytonic way to copy params
        res = self.__class__()
        res._set = new_set
        res.is_async = self.is_async
        res.loop = self.loop
        res.connection_parameters = self.connection_parameters

        return res

    def args_for_set(self, *args):
        # TODO Add named args to args for set ?#

        # transform user arguments into MishmashSet values
        tranformed_arg = []
        for arg in args:
            # if self.is_scalar_mishmash(arg):
            #     tranformed_arg.append(self.get_from_scalar(arg)._set)
            # else:
            if isinstance(arg, Mishmash):
                tranformed_arg.append(arg._set)
            else:
                tranformed_arg.append(arg)

        return tranformed_arg

    def __union(self, *offset):
        # // return a 'united' set
        return self.new_mishmash(self._set.subset().union(*self.args_for_set(*offset)))

    def __intersection(self, *offset):
        # // return a subset
        return self.new_mishmash(self._set.intersection(*self.args_for_set(*offset)))

    def __sync_download(self, stream):
        pass

    async def __async_download(self, stream):

        # async for i in stream.stream(self._set):
        #     s = await i
        #     pprint.pprint(s)
        return await stream.stream(self._set)

    def __anext__():
        raise MishmashNotImplementedYetException("not implemented async next")

    def __download(self):
        stream = MishmashStream()

        s = stream.stream(self._set)
        loop = asyncio.get_event_loop()

        while True:
            try:
                yield loop.run_until_complete(s.__anext__())
            except StopAsyncIteration:
                break

    def __upload(self, base_set, *values):
        # TODO use kwargs args ?
        mutation = MishmashMutation()

        m = mutation.mutate(base_set, *values)

        if not self.loop:
            self.loop = asyncio.get_event_loop()

        try:
            self.loop.run_until_complete(m)
        
        except Exception as e:
            print(e)
