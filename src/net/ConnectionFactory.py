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

    #Todo add get mutation
    
    @staticmethod
    async def __on_send_request(event, options):

        event.metadata['x-mishmash-app-id'] = str(uuid.uuid4()) # todo аpp id == MISHMASHIO_AUTH_APP_ID ?
        event.metadata['authorization'] = "Bearer {}".format(
            options.get_auth_app_id())
            
    @staticmethod
    def set_connection(connection_parameters):

        if ConnectionFactory.__channel:
            return ConnectionFactory.__channel

        if not isinstance(connection_parameters, MishmashConnectionParameters):
            raise WrongConnectionParametersTypeException(" type of connection parameters is {}, it must be MishmashConnectionParameters".format(type(connection_parameters)))

        ConnectionFactory.__channel = Channel(connection_parameters.get_url(), 
                                              connection_parameters.get_port(), 
                                              ssl=connection_parameters.get_use_ssl())
        
        # todo add ssl
        # todo add authentication methods

        if ConnectionFactory.__stub:
            # do i need this check
            raise StubAlreadyCreatedException()

        ConnectionFactory.__stub = mishmash_rpc_grpc.MishmashServiceStub(ConnectionFactory.__channel)

        listen(ConnectionFactory.__channel, 
               SendRequest, 
               lambda event, options = connection_parameters: ConnectionFactory.__on_send_request(event, options))

    @staticmethod
    def close_channel():
        if ConnectionFactory.__channel:
            ConnectionFactory.__channel.close()
            ConnectionFactory.__channel = None
    # do i need close stub method    


class ChannelAlreadyCreatedException(Exception):
    pass


class ChannelHasNotBeenCreatedException(Exception):
    pass


class StubAlreadyCreatedException(Exception):
    pass


class StubHasNotBeenCreatedException(Exception):
    pass
class WrongConnectionParametersTypeException(Exception):
    pass