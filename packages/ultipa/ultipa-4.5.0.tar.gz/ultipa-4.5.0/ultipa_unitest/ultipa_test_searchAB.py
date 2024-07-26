import random
import unittest
from typing import List

from ultipa import ULTIPA_REQUEST, ULTIPA
from ultipa import FILTER
from ultipa_unitest import conn


class TestUltipaMethods(unittest.TestCase):

    gname = 'default'

    def test_search(self):
        ret= conn.searchAB(ULTIPA_REQUEST.SearchAB(src=1,dest=2))
        print(ret.toJSON())