import unittest
from ultipa import *
from ultipa import Connection,ULTIPA_REQUEST,ULTIPA
from ultipa_unitest import conn
import random
from multiprocessing.dummy import Pool as MPThreadPool #线程池


class TestUltipaNormal(unittest.TestCase):

    def test_listproperty(self):

        graphSet=["default", None]
        graphSetName = random.choice(graphSet)
        ret = conn.listProperty(ULTIPA_REQUEST.GetProperty(type=DBType.DBNODE), ULTIPA_REQUEST.Graph(graphSetName))
        self.assertEqual(ret.req.get('graphName'),'default')

        graphSetName = 'Pytest'
        ret = conn.listProperty(ULTIPA_REQUEST.GetProperty(type=DBType.DBNODE),ULTIPA_REQUEST.Graph(graphSetName))
        self.assertEqual(ret.req.get('graphName'), 'Pytest')





