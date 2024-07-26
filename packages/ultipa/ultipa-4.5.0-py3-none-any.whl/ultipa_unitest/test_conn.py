import unittest
from ultipa import *
from ultipa import Connection, ULTIPA_REQUEST, ULTIPA, FILTER
from ultipa.utils.ufilter.new_ufilter import FilterEnum
from ultipa_unitest import conn


class TestUltipaMethods(unittest.TestCase):
    # test 3.0
    gname = 'default'

    # 4.0
    def test_search(self):
        ret = conn.test()
        print(ret)


    def test_InstallALgo(self):
        ret = conn.installAlgo()
        print(ret)
