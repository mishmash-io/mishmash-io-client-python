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
import uuid

from grpclib.client import Channel
from grpclib.events import listen, SendRequest

import mishmash_rpc_grpc
from net.MishmashConnectionParameters import MishmashConnectionParameters




class ConnectionFactory():

    __stub = None
    __channel = None

    @staticmethod
    def get_stream():
        return ConnectionFactory.__stub.stream.open() 

    @staticmethod
    def get_mutation():
        return ConnectionFactory.__stub

    @staticmethod
    async def __on_send_request(event, options):

        event.metadata['x-mishmash-app-id'] = str(uuid.uuid4())
        event.metadata['authorization'] = "Bearer {}".format(
            options.get_auth_app_id())
            
    @staticmethod
    def set_connection(options):

        if not isinstance(options, MishmashConnectionParameters):
            raise Exception("wrong connection parameters type")

        if ConnectionFactory.__channel:
            return ConnectionFactory.__channel
        else:
            ConnectionFactory.__channel = Channel(options.get_url(), 
                                                  options.get_port(), 
                                                  ssl=options.get_use_ssl())

        if ConnectionFactory.__stub:
            raise ChannelHasNotBeenCreatedException


        ConnectionFactory.__stub = mishmash_rpc_grpc.MishmashServiceStub(ConnectionFactory.__channel)

        listen(ConnectionFactory.__channel, 
               SendRequest, 
               lambda event, options = options: ConnectionFactory.__on_send_request(event, options))

    @staticmethod
    def close_channel():
        if ConnectionFactory.__channel:
            ConnectionFactory.__channel.close()
            ConnectionFactory.__channel = None
        


class ChannelAlreadyCreatedException(Exception):
    pass


class ChannelHasNotBeenCreatedException(Exception):
    pass


class StubAlreadyCreatedException(Exception):
    pass


class StubHasNotBeenCreatedException(Exception):
    pass
