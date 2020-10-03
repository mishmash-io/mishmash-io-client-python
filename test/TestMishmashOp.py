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

from MishmashOp import MishmashOp

def test_get_op_id():
    assert MishmashOp.getOpId("__avg"), "avg"
    assert MishmashOp.getOpId("__coalesce"), "coalesce"
    assert MishmashOp.getOpId("__asd") == None
    assert MishmashOp.getOpId("_asd") == None
    assert MishmashOp.getOpId("asd") == None
    assert MishmashOp.getOpId("") == None
    assert MishmashOp.getOpId("__avg1") == None
    assert MishmashOp.getOpId("_avg") == None
    assert MishmashOp.getOpId("___avg") == None