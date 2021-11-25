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

import grpc

import mishmash_rpc_pb2_grpc

from net.MishmashGrpcConfig import MishmashGrpcConfig

class MishmashGrpcClient():
    __grpc_client_instance = None
    
    __channel = None
    __stub = None
    __config = None

    AUTHORIZATION_HEADER_NAME = 'authorization'
    APP_ID_HEADER_NAME = 'x-mishmash-io'

    def __new__(cls):

        if cls.__grpc_client_instance is None:
            
            cls.__grpc_client_instance = super(MishmashGrpcClient, cls).__new__(cls)
            cls.__config = MishmashGrpcConfig()

            if not cls.__config.is_ssl:
                cls.__channel = grpc.aio.insecure_channel(f'{cls.__config.get_server()}')
            else:
                cls.__channel = grpc.aio.secure_channel(f'{cls.__config.get_server()}', 
                                                        grpc.ssl_channel_credentials(cls.__config.trusted_certs))
            
            cls.__stub = mishmash_rpc_pb2_grpc.MishmashServiceStub(cls.__channel)
            
        return cls.__grpc_client_instance

    @classmethod
    def get_stub(cls):
        return cls.__stub

    @classmethod
    def get_auth_metadata(self):
        return grpc.aio.Metadata((MishmashGrpcClient.AUTHORIZATION_HEADER_NAME, 
                                    MishmashGrpcClient.__config.authorization_header),
                                    (MishmashGrpcClient.APP_ID_HEADER_NAME, 
                                    MishmashGrpcClient.__config.app_id))