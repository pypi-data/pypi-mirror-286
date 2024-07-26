import unittest
from ultipa import *
from ultipa import Connection,ULTIPA_REQUEST,ULTIPA
from ultipa_unitest import conn
class TestUltipaMethods(unittest.TestCase):

    #4.0
    def test_lte(self):
        conn.defaultConfig.defaultGraph = "ct_test"
        ret = conn.lte(ULTIPA_REQUEST.LTE(ULTIPA_REQUEST.CommonSchema('default','name'),type=DBType.DBNODE))
        # self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)
        print(ret.toJSON())
        ret.Print()

        # ret = conn.lte(ULTIPA_REQUEST.LTE(ULTIPA_REQUEST.CommonSchema('test', 'name'),
        #                                   type=DBType.DBEDGE))
        # # self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)
        # print(ret.toJSON())


    def test_ufe(self):

        # ret = conn.ufe(ULTIPA_REQUEST.UFE(ULTIPA_REQUEST.CommonSchema('test','name'),type=DBType.DBNODE))
        # # self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)
        # print(ret.toJSON())
        conn.defaultConfig.defaultGraph = "ct_test"

        ret = conn.ufe(ULTIPA_REQUEST.UFE(ULTIPA_REQUEST.CommonSchema('default', 'name'),
                                          type=DBType.DBNODE))
        # self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)
        print(ret.toJSON())
        ret.Print()



