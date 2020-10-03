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

import utils
from async_timeout import timeout
from collections import Counter


import mishmash_rpc_pb2

from net.ConnectionFactory import ConnectionFactory
import net.MishmashMessages as MishmashMessages


class MishmashMutation():

    def __init__(self, mutate_parameters=None):

        self.client_sequence_number = 0
        self.server_sequence_number = 0
        self.cnt = Counter()
        self.index = 0
        self.instance = 0  # TODO add instance in checks

    async def mutate(self, base_set, *values):

        mutation_stub = ConnectionFactory.get_mutation()

        new_connection = True
        has_send_setup_msg = False
        yield_data_msgs = MishmashMessages.to_yield_data(values, self.cnt)

        async with mutation_stub.mutate.open() as mutation:

            while True:

                if new_connection:

                    await mutation.send_message(mishmash_rpc_pb2.MutationClientMessage(
                        client_seq_no=self.client_sequence_number, setup=MishmashMessages.to_setup_msg(base_set)))
                    new_connection = False
                    self.client_sequence_number += 1
         
                async with timeout(utils.RECV_TIMEOUT):

                    recv_msg = await mutation.recv_message()
                
                    if recv_msg:
                        msg_type = MishmashMessages.get_srv_mutation_message_type(recv_msg)

                        if not has_send_setup_msg:
                            if msg_type == "setup_ack":
                                has_send_setup_msg = True
                            else:
                                raise Exception("wrong msg type ", msg_type)
                        else:
                            if msg_type == "error":
                                await self.process_error_message(mutation, recv_msg)

                    try:
                        next_msg = next(yield_data_msgs)
                   
                        await mutation.send_message(mishmash_rpc_pb2.MutationClientMessage(client_seq_no=self.client_sequence_number, yield_data=next_msg))
                        self.client_sequence_number += 1
                   
                    except StopIteration:
                        # recv_msg = await mutation.recv_message()
                        # print(recv_msg)
                        await mutation.end()
                        break
                    
        async def process_error_message(self, stream, recv_msg):
            # TODO add exception type from remote srv
            raise MishmashMutationErrorException(MishmashMessages.to_error_msg(recv_msg))


class MishmashMutationErrorException(Exception):
    # TODO move to_error_msg here
    pass
