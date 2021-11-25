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
from async_timeout import timeout
import grpc
from  mishmash_rpc_pb2 import MutationClientMessage, YieldData, MishmashSetup

from net.MishmashMessageParser import to_stream_setup_msg, to_yield_data, from_yield_value

from net.MishmashGrpcClient import MishmashGrpcClient

from collections import Counter
from MishmashExceptions import MishmashTimeoutException, MishmashInvalidMessageException

class MishmashMutation():
    SETUP_ACK = 1
    YIELD_DATA_ACK = 2
    STREAM_END = 3
    RECV_TIMEOUT_IN_SECONDS = 5 
    def __init__(self):
        # self.__mishmash_set = mishmash_set
        self.iterator = MishmashGrpcClient.get_stub().mutate(metadata=MishmashGrpcClient.get_auth_metadata())
        self.client_seq_no = 1
        self.instance_ids = Counter()
    
    async def send_msg(self, msg):
        await self.iterator.write(msg)

    async def recv_msg(self):
        try:
            async with timeout(MishmashMutation.RECV_TIMEOUT_IN_SECONDS):
                return await self.iterator.read()
        except asyncio.TimeoutError:
            raise MishmashTimeoutException("cannot recv message from server")
    
    async def end_stream(self):
        await self.iterator.done_writing()


    def get_msg_type(self, msg):
        if msg ==  grpc.aio.EOF:
            return MishmashMutation.STREAM_END
        if msg.HasField('setup_ack'):
            return MishmashMutation.SETUP_ACK
        if msg.HasField('ack'):
            return MishmashMutation.YIELD_DATA_ACK
        
    async def send_data(self, mishmash_set, data_iterator):
        await self.send_msg(to_stream_setup_msg(self.get_and_increment_client_seq_no, 
                                            mishmash_set))

        recv_msg = await self.recv_msg()
        recv_msg_type = self.get_msg_type(recv_msg)
        data_message_generator = iter(to_yield_data(data_iterator, self.client_seq_no, self.instance_ids))
        if recv_msg_type != MishmashMutation.SETUP_ACK:
            raise MishmashInvalidMessageException(f"invalid message type {recv_msg_type} ")
        
        for msg, client_id in data_message_generator:
            self.debug(msg)
            self.client_seq_no = client_id
            await self.send_msg(msg)
            recv_msg = await self.recv_msg()
            recv_msg_type = self.get_msg_type(recv_msg)
            if recv_msg_type == MishmashMutation.YIELD_DATA_ACK:
                continue

        await self.end_stream()
    def debug(self,  msg):
        r = []
        def get_name(member):
            if member.HasField("index"):
                return int(member.index)
            elif member.HasField("name"):
                return member.name
        for i in msg.yield_data.hierarchy:
            r .append(f"{get_name(i.member)}<{i.instance_id.id}>")

        value_id, value  = from_yield_value(msg.yield_data.value)

        print(f"{msg.client_seq_no} : {'.'.join(r)} : {value}<{value_id}>")

    def sync_mutation(self, setup_message, data):
        loop = asyncio.get_event_loop()
   
        res = self.send_data(setup_message, data)
        loop.run_until_complete(res)

    async def async_mutation(self, setup_message, data):
    
        return await self.send_data(setup_message, data)

    @property
    def get_and_increment_client_seq_no(self):
        old_seq_no = self.client_seq_no
        self.client_seq_no +=1
        return old_seq_no
    
