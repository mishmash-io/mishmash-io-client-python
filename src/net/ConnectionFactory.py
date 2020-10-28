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


async def on_send_request(event, options):

    request_id = event.metadata['x-mishmash-app-id'] = str(uuid.uuid4())

    event.metadata['authorization'] = "Bearer {}".format(
        options.get_auth_app_id())

    print(f'Generated Request ID: {request_id}')


class ConnectionFactory():

    __stub = None
    __channel = None

    @staticmethod
    def get_stream():
        return ConnectionFactory.__stub

    @staticmethod
    def get_mutation():
        return ConnectionFactory.__stub

    @staticmethod
    def set_connection(options):
        # TODO when i try to create another mishmash it raise ChannelAlreadyCreatedException???

        if not isinstance(options, MishmashConnectionParameters):
            raise Exception("wrong connection parameters type")

        if ConnectionFactory.__channel:
            print("ChannelAlreadyCreatedException")
            return  # TODO HOW TO use this singleton
            raise ChannelAlreadyCreatedException

        if ConnectionFactory.__stub:
            raise ChannelHasNotBeenCreatedException

        if not options.has_ssl_certificates():

            ConnectionFactory.__channel = Channel(
                options.get_url(), options.get_port(), ssl=options.get_use_ssl())

            ConnectionFactory.__stub = mishmash_rpc_grpc.MishmashServiceStub(
                ConnectionFactory.__channel)
            
            listen(ConnectionFactory.__channel, SendRequest, lambda event,
                   options=options: on_send_request(event, options))
        else:
            raise Exception("not implementet yet secure connection type")

    @staticmethod
    def close_channel():
        raise Exception("not implementet yet close_channel type")


class ChannelAlreadyCreatedException(Exception):
    pass


class ChannelHasNotBeenCreatedException(Exception):
    pass


class StubAlreadyCreatedException(Exception):
    pass


class StubHasNotBeenCreatedException(Exception):
    pass
