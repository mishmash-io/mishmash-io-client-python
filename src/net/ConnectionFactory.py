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

from grpclib.client import Channel
from grpclib.events import listen, SendRequest

import mishmash_rpc_grpc

from net.MishmashConnectionParameters import MishmashConnectionParameters
from net.MishmashAuthentication import MishmashAuthentication

class StubAlreadyCreatedException(Exception):
    pass

class WrongConnectionParametersTypeException(Exception):
    pass

class ConnectionFactory():

    __stub = None
    __channel = None
    __authenticator = None

    @staticmethod
    def get_stream():
        return ConnectionFactory.__stub.stream.open()
    
    @staticmethod
    def get_mutation():
        return ConnectionFactory.__stub.mutate.open()

    @staticmethod
    async def __on_send_request(event, options):

        event.metadata['x-mishmash-app-id'] = ConnectionFactory.__authenticator.app_id
        event.metadata['authorization'] =  ConnectionFactory.__authenticator.authorization_header

    @staticmethod
    def set_connection(connection_parameters):

        if ConnectionFactory.__channel:
            return ConnectionFactory.__channel

        if not isinstance(connection_parameters, MishmashConnectionParameters):
            raise WrongConnectionParametersTypeException(
                " type of connection parameters is {}, it must be MishmashConnectionParameters".format(type(connection_parameters)))

        ConnectionFactory.__channel = Channel(connection_parameters.get_url(),
                                              connection_parameters.get_port(),
                                              ssl=connection_parameters.get_use_ssl())

        
        ConnectionFactory.__authenticator = MishmashAuthentication.get_authenticator(connection_parameters.get_auth_method())


        if ConnectionFactory.__stub:
            raise StubAlreadyCreatedException()

        ConnectionFactory.__stub = mishmash_rpc_grpc.MishmashServiceStub(
                                                    ConnectionFactory.__channel)

        listen(ConnectionFactory.__channel,
               SendRequest,
               lambda event, options=connection_parameters: ConnectionFactory.__on_send_request(event, options))

    @staticmethod
    def close_channel():
        if ConnectionFactory.__channel:
            ConnectionFactory.__channel.close()
            ConnectionFactory.__channel = None

