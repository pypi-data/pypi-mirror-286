import unittest
from ultipa import *
from ultipa import Connection,ULTIPA_REQUEST,ULTIPA,ALGO_REQUEST
from ultipa_unitest import conn


class TestUltipaMethods(unittest.TestCase):

    def test_louvain(self):
        ret = conn.louvainDV(ALGO_REQUEST.LouvainDV(1000,2),ULTIPA_REQUEST.Graph())
