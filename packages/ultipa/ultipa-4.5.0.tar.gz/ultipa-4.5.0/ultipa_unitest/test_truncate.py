import unittest
from ultipa import *
from ultipa import Connection,ULTIPA_REQUEST,ULTIPA,FILTER
from ultipa_unitest import conn


class TestUltipaMethods(unittest.TestCase):

    gname = 'default'

    def test_truncate(self):
        ret = conn.truncate(ULTIPA_REQUEST.Truncate(graph='default',truncateType=ULTIPA.TruncateType.NODES,schema="default",allData=True))
        print('>>>>>',ret.toJSON())

    def test_compact(self):
        ret = conn.compact(ULTIPA_REQUEST.Graph(graph='test_py'))
        print(ret.toJSON())