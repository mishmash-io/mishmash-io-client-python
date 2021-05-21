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

from async_timeout import timeout

from net.ConnectionFactory import ConnectionFactory
import net.MishmashMessages as MishmashMessages

import utils

class MishmashStreamErrorException(Exception):
    pass


class MishmashStreamWrongMessageType(Exception):
    pass


class MishmashStream():
    def __init__(self, base_set, stream_parameters=None):

        self.client_seq_no = 0
        self.server_seq_no = 0
        self.results = None
        self.index = 0
        self.instance = 0
        self.base_set = base_set

    async def run(self):

        is_new_connection = True
        setup_msg_has_been_ack = False

        async with ConnectionFactory.get_stream() as stream:

            while True:
                if is_new_connection:
                    await stream.send_message(MishmashMessages.to_setup_msg(self.client_seq_no, self.base_set))
                    is_new_connection = False

                async with timeout(utils.RECV_TIMEOUT):
                    recv_msg = await stream.recv_message()

                    if recv_msg:

                        msg_type = MishmashMessages.get_srv_stream_message_type(
                            recv_msg)

                        if not setup_msg_has_been_ack:
                            if msg_type == "setup_ack":
                                setup_msg_has_been_ack = True
                            else:
                                raise MishmashStreamWrongMessageType(msg_type)
                        else:
                            if msg_type == "yield_data":
                                async for v in self.process_yield_data_message(stream, recv_msg):
                                    yield v
                            elif msg_type == "error":
                                await self.process_error_message(stream, recv_msg)
                            elif msg_type == "invoke":
                                await self.process_invoke_message(stream, recv_msg)
                            elif msg_type == "output":
                                await self.process_output_message(stream, recv_msg)
                            elif msg_type == "debug":
                                await self.process_debug_message(stream, recv_msg)
                    else:

                        if self.results:
                            yield self.results

                        await stream.end()
                        break

    async def process_yield_data_message(self, stream, recv_msg):

        hierarchy, value = MishmashMessages.from_yield_data(recv_msg)

        if not hierarchy:
            yield value

        else:
            if self.index != hierarchy[0].member.index:

                self.index = hierarchy[0].member.index
                self.instance = hierarchy[0].instance_id.id

                yield self.results
                self.results = None

            if self.results is None:

                if hierarchy[1].member.HasField("index"):
                    self.results = []
                else:
                    self.results = {}

            MishmashMessages.process_yield_data_message(
                hierarchy[1:], value, self.results)

        await stream.send_message(MishmashMessages.to_yield_data_ack(self.client_seq_no))

        self.client_seq_no += 1

    async def process_error_message(self, stream, recv_msg):
        # TODO add exception type from remote srv
        raise MishmashStreamErrorException(
            MishmashMessages.to_error_msg(recv_msg))

    async def process_invoke_message(self, stream, recv_msg):
        raise Exception("process invoke msg not implemented yet")

    async def process_output_message(self, stream, recv_msg):
        raise Exception("process output msg not implemented yet")

    async def process_debug_message(self, stream, recv_msg):
        raise Exception("process debug msg not implemented yet")


