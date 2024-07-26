import datetime
import random
import time
import unittest
from datetime import date

from ultipa import *
from ultipa import Connection, ULTIPA_REQUEST, ULTIPA, FILTER
from ultipa_unitest import conn


class TestUltipaMethods(unittest.TestCase):
    gname = 'default'

    def test(self):
        ret = conn.test()
        print(ret)

    #4.0
    def test_search(self):
        ret = conn.showGraph()
        print(ret.toJSON())
        for g in ret.data:
            if g.name.startswith("pytest"):
                conn.dropGraph(ULTIPA_REQUEST.DropGraph(g.name))

    def test_delete_user(self):
        ret = conn.showUser()
        for u in ret.data:
            if u.username.startswith("pytest_u"):
                conn.dropUser(ULTIPA_REQUEST.DropUser(username=u.username))
        print(ret.toJSON())
