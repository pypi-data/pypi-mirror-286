import datetime
from struct import *

from ultipa.proto.ultipa_pb2 import MapData, ListData, SetData
from ultipa.types import ULTIPA
from ultipa.utils.serialize import _Serialize

# def serialize(value):
#     upret = pack('>I', value)
#     return upret
# #
# # ret = serialize(214748364712)
# ret = serialize(-1)
# print(len(ret))
from ultipa.utils.typeCheck import TypeCheck
def test_protoMap():
    map  = MapData()
    rt = map.values.add()
    rt.key = b"asdfasdf"
    rt.value = b"asdfasdfasdfasdf"
    stry = map.SerializeToString()
    print(stry)
    map1 = MapData()
    print(map1.ParseFromString(stry))
    print(map1)

def test_protoList1():
    list1  = ListData()
    list1.values.extend([b"asdfasdf", b"asdfasdfasdfasdf"])
    stry = list1.SerializeToString()
    print(stry)
    map1 = ListData()
    map1.ParseFromString(stry)
    print(map1)

def test_protoSet():
    set1 = SetData()
    set1.values.append(b"asdfasdf")
    stry = set1.SerializeToString()
    print(stry)
    map1 = SetData()
    map1.ParseFromString(stry)
    print(map1)

def test_protoList():
    seria = _Serialize(type=ULTIPA.PropertyType.PROPERTY_LIST, value=["adfasdfasdf","Asdfasdfasdf"],
                       subTypes=[ULTIPA.PropertyType.PROPERTY_STRING])
    ret = seria.serialize()
    print(ret)
    seria = _Serialize(type=ULTIPA.PropertyType.PROPERTY_LIST, value=ret,
                       subTypes=[ULTIPA.PropertyType.PROPERTY_STRING])
    print(seria.unserialize())


if __name__ == '__main__':
    # test_protoList()
    # test_protoMap()
    # test_protoList1()
    test_protoSet()
    # checkRet = TypeCheck.checkProperty(ULTIPA.PropertyType.PROPERTY_INT64, "123123")
    # print(checkRet)

    # try:
    #     ret = _Serialize(value=1.70E308, type=ULTIPA.PropertyType.PROPERTY_DOUBLE).serialize()
    #     print(ret)
    # except Exception as e:
    #     # ret = e.args[0]%(1,1)
    #     # print(type(ret))
    #     print(e)

# uret = unpack('>I',ret)
# print(uret)
# str = '32'
# b = bytes(str,encoding='utf-8')5
# print(b)

# ret = datetime.datetime(2022,8,12,22,11,22)
#
# print(ret)


# ret  = {"id":"1000001","name":"Debra Wheeler","age":"34"}
#
# print(ret.keys())