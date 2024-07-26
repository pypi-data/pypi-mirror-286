import unittest
from ultipa import *
from ultipa import Connection,ULTIPA_REQUEST,ULTIPA
from ultipa_unitest import conn
class TestUltipaMethods(unittest.TestCase):
    #test 3.0
    gname = 'default'
    def test_getleader(self):
        ret = conn.getRaftLeader(requestConfig=RequestConfig())
        print(ret.toJSON())