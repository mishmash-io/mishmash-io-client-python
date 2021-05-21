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
# See the License for the specific language governing permission0s and
# limitations under the License.

from collections import Counter

from async_timeout import timeout

from net.ConnectionFactory import ConnectionFactory
import net.MishmashMessages as MishmashMessages

import utils


class MishmashMutationErrorException(Exception):
    pass

class MishmashMutation():

    def __init__(self,   base_set, *values, mutate_parameters=None):

        self.client_seq_no = 0
        self.server_seq_no = 0
        self.results = None
        self.index = 0
        self.instance = 0
        self.base_set = base_set
        self.values = values
        self.cnt = Counter()

    async def run(self):
        is_new_connection = True

        yield_data_msgs = MishmashMessages.to_yield_data(self.values, self.cnt)

        async with ConnectionFactory.get_mutation() as mutation:
            
            if is_new_connection:
                await mutation.send_message(MishmashMessages.to_mutate_setup_msg(self.client_seq_no, self.base_set))
                is_new_connection = False
                self.client_seq_no += 1
                recv_msg = await mutation.recv_message()
                
                if MishmashMessages.get_srv_mutation_message_type( recv_msg) != "setup_ack":
                    await self.process_error_message(mutation, recv_msg)

            async with timeout(utils.RECV_TIMEOUT):
                for i, next_msg in enumerate(yield_data_msgs):
                    await mutation.send_message(MishmashMessages.to_mutation_client_msg(self.client_seq_no, next_msg))   
                    self.client_seq_no += 1
                    recv_msg = await mutation.recv_message()
 
                    
                    if MishmashMessages.get_srv_mutation_message_type( recv_msg) != "ack":
                        await self.process_error_message(mutation, recv_msg)
                await mutation.end()
            
    
       
    async def process_error_message(self, stream, recv_msg):
        raise MishmashMutationErrorException(
            MishmashMessages.to_error_msg(recv_msg))

