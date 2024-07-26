import time
import unittest

from ultipa_unitest import conn
from ultipa_unitest.helper import GetTestConnection
from ultipa import Connection, ULTIPA_REQUEST, ULTIPA
import random


class TestUltipaMethods(unittest.TestCase):

    def test_raft(self):
        # conn.test()
        ret = conn.getRaftLeader()
        print(ret.status.clusterInfo.leader)
        # time.sleep(120)
        # ret = conn.getRaftLeader(RequestConfig(graphName="amz"))
        # print(ret.toJSON())
        # ret = conn.clusterInfo()
        # print(ret.toJSON())
        # ret = conn.listUser(RequestConfig())
        # print(ret.toJSON())
        # ret = conn.listUser(RequestConfig())
        # print(ret.toJSON())
        # ret = conn.listUser(RequestConfig())
        # print(ret.toJSON())
        # ret = conn.listUser(RequestConfig())
        # print(ret.toJSON())
        "".format()



    def test_uql(self):
        # ret = conn.uql('alter().graph("test_graph124").set({"name": "test_graph125"})')
        ret = conn.uql('show().task()')
        print(ret.toJSON())
        assert ret.status.code == ULTIPA.Code.SUCCESS
