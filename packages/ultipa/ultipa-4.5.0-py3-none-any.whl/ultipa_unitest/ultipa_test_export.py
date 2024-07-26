import json
import unittest
from ultipa import *
from ultipa import Connection, ULTIPA_REQUEST, ULTIPA
from ultipa_unitest import conn
import random


class testultipamethods(unittest.TestCase):
	gname = 'default'

	def test_export_edge(self):
		ret = conn.export(
			ULTIPA_REQUEST.Export(type=DBType.DBEDGE, schema="amz", limit=10, properties=['name', 'age']),
			RequestConfig(graphName=self.gname))
		print(ret.toJSON())

	def test_export_node(self):
		ret = conn.export(ULTIPA_REQUEST.Export(type=DBType.DBNODE, schema="amz", limit=2, properties=['name']),
						  RequestConfig(graphName=self.gname))
		print(ret.toJSON())
