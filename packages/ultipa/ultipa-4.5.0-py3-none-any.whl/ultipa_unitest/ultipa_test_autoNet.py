import unittest
from ultipa import *
from ultipa import Connection,ULTIPA_REQUEST,ULTIPA
from ultipa_unitest import conn
import random

class TestUltipaMethods(unittest.TestCase):
    gname = 'default'

    def test_autoNet(self):
        ret = conn.getGraph(ULTIPA_REQUEST.Graph(self.gname),RequestConfig())
        node_ret = ret.data.get('totalNodes')
        edge_ret = ret.data.get('totalEdges')
        # for i in range(1000):
        srcs = [self.random_node(node_ret) for i in range(random.randint(1,10))]
        # ret = conn.autoNet(ULTIPA_REQUEST.AutoNet(srcs=srcs,depth=3,limit=2))
        # self.assertEqual(ret.status.code,ULTIPA.Code.SUCCESS)

        dets = [self.random_node(node_ret) for i in range(random.randint(1,10))]
        ret = conn.autoNet(ULTIPA_REQUEST.AutoNet(srcs=srcs,dests=dets,depth=3,limit=2,select=['name']),RequestConfig(graphSetName=self.gname))
        print(ret.toJSON())
        self.assertEqual(ret.status.code,ULTIPA.Code.SUCCESS)

    def random_node(self,noderet):
        nodeid = str(random.randint(1,int(noderet)))
        return nodeid

    def test_autoNet_flow(self):
        # ret = conn.autoNet(ULTIPA_REQUEST.AutoNet(srcs=['12'],dests=['21','270336','18432'],depth=3,limit=10,select=['name']),ULTIPA_REQUEST.Graph(self.gname))
        # print(ret.toJSON())

        auFilter = ULTIPA_REQUEST.FILTER.EqFilter('name','Like')
        ret = conn.autoNet(
            ULTIPA_REQUEST.AutoNet(srcs=[12], dests=[21, 270336, 18432],edge_filter=auFilter.builder(),depth=3, limit=30, select=['name'],no_circle=True,turbo=True,boost=True,shortest=True),
            RequestConfig(self.gname))
        # print(ret.data.toJSON())
        print(ret.toJSON())