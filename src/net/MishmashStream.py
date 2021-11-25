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

import grpc

from async_timeout import timeout

from  mishmash_rpc_pb2 import StreamClientMessage, YieldDataAck, MishmashSetup
from net.MishmashMessageParser import to_stream_setup_msg,  from_yield_data, process_yield_data_message,get_container_for_next_element
from net.MishmashGrpcClient import MishmashGrpcClient

from MishmashExceptions import MishmashTimeoutException, MishmashInvalidMessageException

class MishmashStream():
    
    SETUP_ACK = 1
    YIELD_DATA = 2
    STREAM_END = 3
    RECV_TIMEOUT_IN_SECONDS = 5 
    def __init__(self, mishmash_set):
        self.__mishmash_set = mishmash_set
        self.iterator = MishmashGrpcClient.get_stub().stream(metadata=MishmashGrpcClient.get_auth_metadata())
        self.client_seq_no = 1
        self.index = 0
        self.results  = None
    
    async def send_msg(self, msg):
        await self.iterator.write(msg)

    async def recv_msg(self):
        try:
            async with timeout(MishmashStream.RECV_TIMEOUT_IN_SECONDS):
                return await self.iterator.read()
        except asyncio.TimeoutError:
            raise MishmashTimeoutException("cannot recv message from server")
    
    def get_msg_type(self, msg):
        if msg ==  grpc.aio.EOF:
            return MishmashStream.STREAM_END
        if msg.HasField('setup_ack'):
            return MishmashStream.SETUP_ACK
        if msg.HasField('yield_data'):
            return MishmashStream.YIELD_DATA
        
    
    async def get_data(self, setup_message):
        await self.send_msg(setup_message)

        recv_msg = await self.recv_msg()
        recv_msg_type = self.get_msg_type(recv_msg)
        if recv_msg_type != MishmashStream.SETUP_ACK:
            raise MishmashInvalidMessageException(f"invalid message type {recv_msg_type} ")
       
        while True:

            recv_msg = await self.recv_msg()
            recv_msg_type = self.get_msg_type(recv_msg)
            
            if recv_msg_type == MishmashStream.STREAM_END:
                if self.results:
                    yield self.results

                break 

            if recv_msg_type == MishmashStream.YIELD_DATA:
                async for v in self.process_yield_data_message(recv_msg):
                    yield v
 
                self.client_seq_no += 1
                await self.send_msg(StreamClientMessage(client_seq_no=self.client_seq_no,
                                                        ack=YieldDataAck()))
            else:
                raise MishmashInvalidMessageException(f"invalid message type {recv_msg_type} , {recv_msg}")

    async def process_yield_data_message(self, recv_msg):
        hierarchy, value, instance_id = from_yield_data(recv_msg)

        if not hierarchy:
            yield value

        else:
            if self.index != hierarchy[0].member.index:

                self.index = hierarchy[0].member.index
                self.instance = hierarchy[0].instance_id.id
                yield self.results
                self.results = None
                # return self.results

            if self.results is None:
                self.results = get_container_for_next_element(hierarchy[1].member)

            process_yield_data_message(
                hierarchy[1:], value, self.results)


        self.client_seq_no += 1


    def sync_stream(self):
        
        setup_message = to_stream_setup_msg(self.get_and_increment_client_seq_no, 
                                            self.__mishmash_set)

        loop = asyncio.get_event_loop()

        data = self.get_data(setup_message)

        while True:
            try:
                res = data.__anext__()
                yield loop.run_until_complete(res)
            except StopAsyncIteration:
                break
            except asyncio.CancelledError:
                print('Tasks has been canceled')
    
    async def async_stream(self):
        
        setup_message = to_stream_setup_msg(self.get_and_increment_client_seq_no, 
                                            self.__mishmash_set)

        data = self.get_data(setup_message)

        async for i in data:
            yield i

    @property
    def get_and_increment_client_seq_no(self):
        old_seq_no = self.client_seq_no
        self.client_seq_no +=1
        return old_seq_no
    