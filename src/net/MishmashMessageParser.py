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

from datetime import datetime
from MishmashExceptions import MishmashNotImplementedYetException, MishmashInvalidMessageException

import mishmash_rpc_pb2
from MishmashSet import MishmashSet
from MishmashFunction import MishmashFunction
from MishmashLiteral import MishmashLiteral
import utils

MUTATION_TYPE_OVERWRITE ='overwrite'
MUTATION_TYPE_APPEND ='append'


def to_id(arg):
    if isinstance(arg, str):
        return mishmash_rpc_pb2.Id(id=arg)
    else:
        return mishmash_rpc_pb2.Id(id=str(arg))
        

def to_member(arg):
    if isinstance(arg, int):
        return mishmash_rpc_pb2.Member(index=arg)
    elif isinstance(arg, str):
        return mishmash_rpc_pb2.Member(name=arg)
    else:
        raise MishmashInvalidMessageException("wrong member type for arg = ", arg, type(arg))


def to_decimal(arg):
    # TODO ADD OTHER string_sequence, big_decimal

    if isinstance(arg, int):
        return mishmash_rpc_pb2.DecimalValue(s_int_64=arg)
    elif isinstance(arg, float):
        return mishmash_rpc_pb2.DecimalValue(floating=arg)



def to_yield_member(arg, _id):
    return mishmash_rpc_pb2.YieldMember(member=to_member(arg), instance_id=to_id(_id))


def to_yield_value(arg, _id):
    return mishmash_rpc_pb2.YieldValue(value=to_value(arg), instance_id=to_id(_id))


def to_litearal(arg):
    if isinstance(arg, mishmash_rpc_pb2.Id):
        return mishmash_rpc_pb2.Literal(id=arg)

    elif isinstance(arg, mishmash_rpc_pb2.Value):
        return mishmash_rpc_pb2.Literal(value=arg)

    else:
        raise MishmashInvalidMessageException("wrong member type for arg = ", arg, type(arg))


def to_value(arg):
    if isinstance(arg, int):
        return mishmash_rpc_pb2.Value(decimal=to_decimal(arg))
    elif isinstance(arg, bool):
        return mishmash_rpc_pb2.Value(boolean=mishmash_rpc_pb2.BooleanValue(boolean=arg))
    elif arg is None:
        return mishmash_rpc_pb2.Value(null=mishmash_rpc_pb2.NullValue())
    elif isinstance(arg, float):
        return mishmash_rpc_pb2.Value(decimal=to_decimal(arg))
    elif isinstance(arg, str):
        return mishmash_rpc_pb2.Value(string=mishmash_rpc_pb2.StringValue(sequence=arg))
    elif utils.isinstance_datetime(arg):
        return mishmash_rpc_pb2.Value(date=mishmash_rpc_pb2.DateValue(iso8601=arg.isoformat()))
    else:
        raise MishmashNotImplementedYetException(f"value with type {type(arg)} is not implemented yet")
    # TODO add buffer


def to_function_body(arg):
    return mishmash_rpc_pb2.LambdaFunctionBody(source=arg)


def to_lambda_function_closure(arg):
    l = []
    for k, v in arg.parameters.items():
        # TODO how to pass args
        closure = mishmash_rpc_pb2.LambdaFunctionClosure()
        closure.identifier = str(v)
        l.append(closure)

    return l


def to_lambda_function(arg):
    # TODO only body or whole function source ?
    function_scope = to_lambda_function_closure(arg.clojure)
    return mishmash_rpc_pb2.LambdaFunction(client_runtime=arg.client_runtime,
                                           name=arg.name,
                                           scope_id=arg.scope_id,
                                           body=to_function_body(arg.body),
                                           scope=function_scope)


def to_set_descriptor_list(target_set):

    def populate_set_descriptor_list(target_set, set_descriptors):
        
        if isinstance(target_set, MishmashSet):
            
            descriptor_list = set_descriptors.entries.add(intersection=mishmash_rpc_pb2.Intersection(
                sets=mishmash_rpc_pb2.MishmashSetDescriptorList()))

            if not target_set.get_def():
                return descriptor_list

            populate_set_descriptor_list(
                target_set.get_def(), descriptor_list.intersection.sets)

        elif isinstance(target_set, list):
            descriptor_list = set_descriptors.entries.add(union=mishmash_rpc_pb2.Union(
                sets=mishmash_rpc_pb2.MishmashSetDescriptorList()))

            for v in target_set:
                populate_set_descriptor_list(v, descriptor_list.union.sets)

        elif isinstance(target_set, MishmashFunction):
            set_descriptors.entries.add(
                lambda_function=to_lambda_function(target_set))

        elif isinstance(target_set, MishmashLiteral):
            # TODO can we have id literal or we can have only value literal check proto file
            set_descriptors.entries.add(literal=mishmash_rpc_pb2.Literal(
                value=to_value(target_set.get_literal())))

        else:
            raise Exception(
                "wrong type passed to descriptor list", type(target_set))

    descriptor_list = mishmash_rpc_pb2.MishmashSetDescriptorList()
    populate_set_descriptor_list(target_set, descriptor_list)

    return descriptor_list


def to_yield_data_ack(client_seq_no):

    return mishmash_rpc_pb2.StreamClientMessage(
        client_seq_no=client_seq_no, ack=mishmash_rpc_pb2.YieldDataAck())


def to_client_invoke_result(client_seq_no, ack_seq_no, result):

    return mishmash_rpc_pb2.StreamClientMessage(
        client_seq_no=client_seq_no, invoke_result=mishmash_rpc_pb2.ClientInvokeResult(ack_seq_no=ack_seq_no, result=to_value(result)))


def to_console_output_ack(client_seq_no, ack_seq_no):

    return mishmash_rpc_pb2.StreamClientMessage(
        client_seq_no=client_seq_no, output_ack=mishmash_rpc_pb2.ConsoleOutputAck(ack_seq_no=ack_seq_no))


def to_debug_ack(client_seq_no, ack_seq_no):

    return mishmash_rpc_pb2.StreamClientMessage(
        client_seq_no=client_seq_no, debug_ack=mishmash_rpc_pb2.DebugAck(ack_seq_no=ack_seq_no))

def from_client_invoke_request(invoke_request):

    return invoke_request.callable_id


def to_mutation_type(str_mutation_type):
    if str_mutation_type == MUTATION_TYPE_OVERWRITE:
        return mishmash_rpc_pb2.MishmashSetup.MutationType.OVERWRITE
    elif str_mutation_type == MUTATION_TYPE_APPEND:
        return mishmash_rpc_pb2.MishmashSetup.MutationType.APPEND
    else:
        return mishmash_rpc_pb2.MishmashSetup.MutationType.APPEND



def to_stream_setup_msg(client_seq_no, base_set, mutation_type=None,client_options=None):
    
    if not client_options:
        client_options = {}

    return mishmash_rpc_pb2.StreamClientMessage(
        client_seq_no=client_seq_no,
        setup=mishmash_rpc_pb2.MishmashSetup(target_set=to_set_descriptor_list(base_set),
                                             client_options=client_options,
                                             mutation_type=to_mutation_type(mutation_type)))



def to_mutate_setup_msg(client_seq_no, base_set, mutation_type , client_options=None):
    if not client_options:
        client_options = {}
    
    return mishmash_rpc_pb2.MutationClientMessage(
        client_seq_no=client_seq_no,
        setup=mishmash_rpc_pb2.MishmashSetup(target_set=to_set_descriptor_list(base_set),
                                             client_options=client_options,
                                             mutation_type=to_mutation_type(mutation_type)))



def dummy_descriptor_list():
    # TODO delete me
    print("\n\n\n--------------USING DUMMY DESCRIPTOR LIST----------------- \n\n\n")
    descriptor_list = mishmash_rpc_pb2.MishmashSetDescriptorList()
    descriptor_list.entries.add(
        literal=mishmash_rpc_pb2.Literal(value=to_value("asdf")))
    return descriptor_list


def from_decimal(decimal):

    if decimal.HasField("u_int_32"):
        return int(decimal.u_int_32)
    elif decimal.HasField("s_int_32"):
        return int(decimal.s_int_32)
    elif decimal.HasField("u_int_64"):
        return int(decimal.u_int_64)
    elif decimal.HasField("s_int_64"):
        return int(decimal.s_int_64)
    elif decimal.HasField("floating"):
        return float(decimal.floating)
    elif decimal.HasField("string_sequence"):
        raise MishmashNotImplementedYetException("string_sequence not implemented yet")
    elif decimal.HasField("big_decimal"):
        raise MishmashNotImplementedYetException("big_decimal not implemented yet")
    else:
        raise MishmashNotImplementedYetException("wrong decimal value")


def from_string(string):
    return string.sequence


def from_boolean(boolean):
    return boolean.boolean


def from_value(value):
    if value.HasField("boolean"):
        return from_boolean(value.boolean)
    elif value.HasField("decimal"):
        return from_decimal(value.decimal)
    elif value.HasField("string"):
        return from_string(value.string)
    elif value.HasField("date"):
        return datetime.strptime(value.date.iso8601, "%Y-%m-%dT%H:%M:%SZ")
    elif value.HasField("buffer"):
        raise MishmashNotImplementedYetException("get buffer not implemented yet")
    elif value.HasField("null"):
        return None
    else:
        raise MishmashInvalidMessageException(
            "wrong value = {} with type = {}".format(value, type(value)))


def from_litearal(arg):
    if arg.HasField("id"):
        return from_id(arg.id)
    elif arg.HasField("value"):
        return from_value(arg.value)

    else:
        raise MishmashInvalidMessageException("wrong member type for arg = ", arg, type(arg))


def from_id(_id):
    return _id.id


def from_yield_value(yield_value):
    return from_id(yield_value.instance_id), from_value(yield_value.value)


def from_yield_data(yield_data):

    instance_id, value = from_yield_value(yield_data.yield_data.value)

    return yield_data.yield_data.hierarchy, value, instance_id


def get_key_from_member(member):
    if member.HasField("index"):
        return int(member.index)
    elif member.HasField("name"):
        return member.name


def get_container_for_next_element(member):
    if member.HasField("index"):
        return []
    elif member.HasField("name"):
        return {}


def process_yield_data_message(hierarchy, value, results):

    key = get_key_from_member(hierarchy[0].member)

    if len(hierarchy) > 1:

        next_element_container = get_container_for_next_element(
            hierarchy[1].member)

        if hierarchy[0].member.HasField("index"):
            if len(results) <= key:
                results.append(next_element_container)
        else:
            if not key in results:
                results[key] = next_element_container

        process_yield_data_message(hierarchy[1:], value, results[key])

    else:
        results[key] = value


import pprint

def to_yield_data(y, client_seq_no, instance_id):
    
    def flatten(x, name=[]):
        nonlocal client_seq_no
        if type(x) is dict:
            for idx in x:
                instance_id[idx] += 1
                yield from flatten(x[idx], name + [to_yield_member(idx, instance_id[idx]-1)])
                

        elif isinstance(x, (list, tuple)):
            for idx, v in enumerate(x):
                instance_id[idx] += 1
                yield from flatten(v, name + [to_yield_member(idx, instance_id[idx]-1)])
                
        else:
            instance_id[x] += 1
            client_seq_no += 1
            yield mishmash_rpc_pb2.MutationClientMessage(client_seq_no=client_seq_no, yield_data=mishmash_rpc_pb2.YieldData(hierarchy=name, value=to_yield_value(x, instance_id[x]-1))), client_seq_no
            

    yield from flatten(y)


def from_setup_msg(setup_msg):
    # TODO
    result_set = []

    if isinstance(setup_msg, mishmash_rpc_pb2.MishmashSetDescriptorList):
        for i in setup_msg.entries:
            result_set.append(from_setup_msg(i))
    elif isinstance(setup_msg, mishmash_rpc_pb2.MishmashSetDescriptor):

        if setup_msg.HasField("intersection"):

            result_set = MishmashSet()
            result_set._MishmashSet__def.append(
                from_setup_msg(setup_msg.intersection.sets))

        elif setup_msg.HasField("union"):
            result_set = from_setup_msg(setup_msg.union.sets)
            # result_set.append()
        elif setup_msg.HasField("literal"):
            result_set = MishmashLiteral(from_litearal(setup_msg.literal))

    return result_set


def get_srv_stream_message_type(reply):
    if reply.HasField("yield_data"):
        return "yield_data"
    elif reply.HasField("setup_ack"):
        return "setup_ack"
    elif reply.HasField("error"):
        return "error"
    elif reply.HasField("invoke"):
        return "invoke"
    elif reply.HasField("output"):
        return "output"
    elif reply.HasField("debug"):
        return "debug"
    else:
        raise MishmashInvalidMessageException(f"no such type {reply}" )


def get_srv_mutation_message_type(reply):
    if not reply:
        return None
    if reply.HasField("ack"):
        return "ack"
    elif reply.HasField("setup_ack"):
        return "setup_ack"
    elif reply.HasField("error"):
        return "error"
    else:
        raise MishmashInvalidMessageException("no such type", reply)


def to_error_msg(error):

    error_msg = "\n\terror_code = {}\n\tmessage = {}".format(
        error.error.error_code, error.error.message)
    try:
        additional_info_msg = ""
        for i in error.error.additional_info:
            additional_info_msg += "\n\t{}".format(i)
        if additional_info_msg:
            error_msg += additional_info_msg
    except:
        pass

    return error_msg

def to_mutation_client_msg(client_seq_no, yield_data):
    return mishmash_rpc_pb2.MutationClientMessage(client_seq_no=client_seq_no, yield_data=yield_data)