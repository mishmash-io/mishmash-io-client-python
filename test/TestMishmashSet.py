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

import MishmashSet

#TODO what is scalar and should i use it like php ? 

def test_UnionWithScalars():
    scalar_set = MishmashSet.MishmashSet()

    scalar_set.union(True)
    assert scalar_set.getDef()[0].getType() == "u"
    assert scalar_set.getDef()[0].getLiteral() == True

    scalar_set.union(1)
    assert scalar_set.getDef()[0][1].getType() == "u"
    assert scalar_set.getDef()[0][1].getLiteral() == 1

    scalar_set.union(12.35)
    assert scalar_set.getDef()[0][2].getType() == "u"
    assert scalar_set.getDef()[0][2].getLiteral() == 12.35

    scalar_set.union("asdf")
    assert scalar_set.getDef()[0][3].getType() == "u"
    assert scalar_set.getDef()[0][3].getLiteral() == "asdf"
    
    scalar_set.union("__asdf")
    assert scalar_set.getDef()[0][4].getType() == "u"
    assert scalar_set.getDef()[0][4].getLiteral() == "__asdf"

    scalar_set.union("_avg")
    assert scalar_set.getDef()[0][5].getType() == "u"
    assert scalar_set.getDef()[0][5].getLiteral() == "_avg"

    scalar_set.union("__avg")
    assert scalar_set.getDef()[0][6].getType() == "o"
    assert scalar_set.getDef()[0][6].getLiteral() == "avg"

def test_IntersectionWithScalars():
    scalar_set = MishmashSet.MishmashSet()

    scalar_set = scalar_set.intersection(True)
    assert scalar_set.getDef()[0].getType() == "u"
    assert scalar_set.getDef()[0].getLiteral() == True

    scalar_set = scalar_set.intersection(1)
    assert scalar_set.getDef()[1].getType() == "u"
    assert scalar_set.getDef()[1].getLiteral() == 1

    scalar_set = scalar_set.intersection(12.35)
    assert scalar_set.getDef()[2].getType() == "u"
    assert scalar_set.getDef()[2].getLiteral() == 12.35

    scalar_set = scalar_set.intersection("asdf")
    assert scalar_set.getDef()[3].getType() == "u"
    assert scalar_set.getDef()[3].getLiteral() == "asdf"
    
    scalar_set = scalar_set.intersection("__asdf")
    assert scalar_set.getDef()[4].getType() == "u"
    assert scalar_set.getDef()[4].getLiteral() == "__asdf"

    scalar_set = scalar_set.intersection("_avg")
    assert scalar_set.getDef()[5].getType() == "u"
    assert scalar_set.getDef()[5].getLiteral() == "_avg"

    scalar_set = scalar_set.intersection("__avg")
    assert scalar_set.getDef()[6].getType() == "o"
    assert scalar_set.getDef()[6].getLiteral() == "avg"

def test_unionWithEmptyObject():
    
    first_set = MishmashSet.MishmashSet()
    first_set.union(1)
    
    second_set = MishmashSet.MishmashSet()
    first_set.union(second_set)

    assert first_set.getDef()[0][0].getType() == "u"
    assert first_set.getDef()[0][0].getLiteral() == 1 

    assert bool(first_set.getDef()[0][1]) == True

def test_unionObject():
    first_set = MishmashSet.MishmashSet()
    first_set.union(0,1,2)
    second_set = MishmashSet.MishmashSet()
    # second_set.union(first_set)
    # print(second_set)
    # assert second_set.getDef()[0].getDef()[0].getDef()[0].getType() == "u"
    # assert second_set.getDef()[0].getDef()[0].getDef()[0].getLiteral() == 0

    # second_set.union(1)
    # second_set.union(2)
    # print(second_set)
    # assert second_set.getDef()[0][1].getType() == "u"
    # assert second_set.getDef()[0][1].getLiteral() == 12
    # assert second_set.getDef()[0][2].getType() == "u"
    # assert second_set.getDef()[0][2].getLiteral() == 2

def test_intersectionObject():
    first_set = MishmashSet.MishmashSet()
    first_set.union(1, True, "asdf")
    second_set = MishmashSet.MishmashSet()
    second_set = second_set.intersection(first_set)
    assert second_set.getDef()[0].getDef()[0][0].getType() == "u"
    assert second_set.getDef()[0].getDef()[0][0].getLiteral() == 1

def test_subset():
    first_set = MishmashSet.MishmashSet()
    first_set.union(1)
    subset = first_set.subset()

    assert subset.getDef()[0].getType() == "u"
    assert subset.getDef()[0].getLiteral() == 1
    assert subset.getDef()[1] == []


def test_SubsetWithOtherSet():
    first_set = MishmashSet.MishmashSet()
    first_set.union(1)
    second_set = MishmashSet.MishmashSet()
    second_set.union(first_set)
    subset = second_set.subset()
    # todo
    # print(subset.getDef()[0])
    assert subset.getDef()[0].getDef()[0].getType() == "u"
    assert subset.getDef()[0].getDef()[0].getLiteral() == 1
    assert subset.getDef()[1] == []


def test_intersectList():
    mishmash_set = MishmashSet.MishmashSet()

    mishmash_set = mishmash_set.intersection([1,2,3],4)
    print(mishmash_set.getDef()[0][0])


    assert mishmash_set.getDef()[0][0].getLiteral() == 1
    assert mishmash_set.getDef()[0][1].getLiteral() == 2
    assert mishmash_set.getDef()[0][2].getLiteral() == 3
    assert mishmash_set.getDef()[1].getLiteral() == 4

