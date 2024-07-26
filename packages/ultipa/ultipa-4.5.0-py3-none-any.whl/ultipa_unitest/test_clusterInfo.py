import unittest
from ultipa import *
from ultipa import Connection,ULTIPA_REQUEST,ULTIPA,FILTER
from ultipa_unitest import conn


class TestUltipaMethods(unittest.TestCase):

    gname = 'default'

    def test_cluster(self):
        ret = conn.clusterInfo()
        print('>>>>>',ret.toJSON())