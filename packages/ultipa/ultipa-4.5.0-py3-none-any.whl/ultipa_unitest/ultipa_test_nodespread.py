import unittest
from ultipa import *
from ultipa import ULTIPA_REQUEST,ULTIPA
from ultipa_unitest import conn

class TestUltipaMethods(unittest.TestCase):

    gname = 'default'

    def test_nodeSpread(self):
        ret = conn.nodeSpread(ULTIPA_REQUEST.NodeSpread(src=12,depth=1,limit=10))
        print(ret.toJSON())
        self.assertEqual(ret.status.code,ULTIPA.Code.SUCCESS)

        # ret = conn.nodeSpread(ULTIPA_REQUEST.NodeSpread(src='12', depth=2, limit=10),ULTIPA_REQUEST.Graph(self.gname))
        # self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)
        #
        # ret = conn.nodeSpread(ULTIPA_REQUEST.NodeSpread(src='12', depth=3, limit=10),ULTIPA_REQUEST.Graph(self.gname))
        # self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)
        #
        # ret = conn.nodeSpread(ULTIPA_REQUEST.NodeSpread(src='12', depth=5, limit=10),ULTIPA_REQUEST.Graph(self.gname))
        # self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)
        #
        # ret = conn.nodeSpread(ULTIPA_REQUEST.NodeSpread(src='12', depth=0, limit=10),ULTIPA_REQUEST.Graph(self.gname))
        # # print(ret.toJSON())
        # self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)

    def test_nodeSpread_Filter(self):
        nofilter= ULTIPA_REQUEST.FILTER.EqFilter('age',20)
        ret = conn.nodeSpread(ULTIPA_REQUEST.NodeSpread(src=12, depth=1, limit=10,node_filter=nofilter.builder(),select_node_properties=['*']),
                              ULTIPA_REQUEST.Graph(self.gname))
        print(ret.toJSON())
        self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)

    def test_nodeSpreadtest(self):
        ret = conn.nodeSpread(ULTIPA_REQUEST.NodeSpread(src=12,depth=1,limit=10))
        print(ret.toJSON())
        print(ret.data.toJSON())
        self.assertEqual(ret.status.code,ULTIPA.Code.SUCCESS)


    def test_timeOut(self):
        ret = conn.nodeSpread(ULTIPA_REQUEST.NodeSpread(src=12,depth=1,limit=10))
        print(ret.toJSON())

    def test_O(self):
        ret = conn.nodeSpread(ULTIPA_REQUEST.NodeSpread(osrc='1',depth=1,limit=10))
        print(ret.toJSON())
