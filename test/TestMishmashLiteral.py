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

import pytest

import MishmashLiteral

record_literal = "r"
field_literal = "f"
value_literal = "v"
op_literal = "o"
unknown_literal = "u"
param_set = "p"

def test_emptyLiteral():
    mishmash_literal = MishmashLiteral.MishmashLiteral()
    
    assert mishmash_literal.isUnknown() == True
    assert mishmash_literal.getType() == unknown_literal
    assert mishmash_literal.getLiteral() == None

def test_RecordType():

    mishmash_literal = MishmashLiteral.MishmashLiteral(None, record_literal)

    assert mishmash_literal.isRecord() == True
    assert mishmash_literal.getType() == record_literal

def test_FieldType():

    mishmash_literal = MishmashLiteral.MishmashLiteral(None, field_literal)

    assert mishmash_literal.isField() == True
    assert mishmash_literal.getType() == field_literal

def test_ValueType():

    mishmash_literal = MishmashLiteral.MishmashLiteral(None, value_literal)

    assert mishmash_literal.isValue() == True
    assert mishmash_literal.getType() == value_literal

def test_OpType():

    mishmash_literal = MishmashLiteral.MishmashLiteral(None, op_literal)

    assert mishmash_literal.isOp() == True
    assert mishmash_literal.getType() == op_literal

def test_UnknownType():

    mishmash_literal = MishmashLiteral.MishmashLiteral(None, unknown_literal)

    assert mishmash_literal.isUnknown() == True
    assert mishmash_literal.getType() == unknown_literal

    mishmash_literal = MishmashLiteral.MishmashLiteral(None, unknown_literal)
    assert mishmash_literal.isUnknown() == True
    assert mishmash_literal.getType() == unknown_literal

def test_boolean():
    boolean_lit = MishmashLiteral.MishmashLiteral.boolean(True)

    assert boolean_lit.getLiteral() == True
    assert boolean_lit.getType() == unknown_literal

def test_integer():
    integer_lit = MishmashLiteral.MishmashLiteral.integer(1234)

    assert integer_lit.getLiteral() == 1234
    assert integer_lit.getType() == unknown_literal

def test_double():
    double_lit = MishmashLiteral.MishmashLiteral.double(12.34)

    assert double_lit.getLiteral() == 12.34
    assert double_lit.getType() == unknown_literal

def test_string():
    string_lit = MishmashLiteral.MishmashLiteral.string("asdf")

    assert string_lit.getLiteral() == "asdf"
    assert string_lit.getType() == unknown_literal


def test_op_as_string_without_prefix():
    string_lit = MishmashLiteral.MishmashLiteral.string("avg")

    assert string_lit.getLiteral() == "avg"
    assert string_lit.getType() == unknown_literal

def test_op_as_string_with_prefix():
    string_lit = MishmashLiteral.MishmashLiteral.string("__avg")

    assert string_lit.getLiteral() == "avg"
    assert string_lit.getType() == op_literal

def test_null():
    null_lit = MishmashLiteral.MishmashLiteral.null()

    assert null_lit.getLiteral() == None
    assert null_lit.getType() == unknown_literal

#TODO test_jsonSerialize_without_param
#TODO test_jsonSerialize_without_param_with_op
#TODO test_jsonSerialize_with_param
#TODO add test parameter with mishmashset with values
#TODO add test for from json
#TODO add test for prettyPrint
#TODO add tests for array object resource exception 










