import unittest

from ultipa import ULTIPA_REQUEST, ULTIPA
from ultipa_unitest import conn


class TestUltipaMethods(unittest.TestCase):

    def test_delete_pytest_graph(self):
        ret = conn.listGraph(RequestConfig())
        for i in ret.data:
            if i.name.startswith('pytest'):
                conn.dropGraph(ULTIPA_REQUEST.DropGraph(graphSetName=i.name))
