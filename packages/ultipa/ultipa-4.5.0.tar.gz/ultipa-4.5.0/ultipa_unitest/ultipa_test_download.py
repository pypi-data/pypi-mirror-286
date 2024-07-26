import unittest
from ultipa import *
from ultipa import Connection, ULTIPA_REQUEST, ULTIPA
from ultipa_unitest import conn


class TestUltipaMethods(unittest.TestCase):

	def test_download(self):
		ret = conn.download(ULTIPA_REQUEST.Download("amz_ids", 31),
							RequestConfig(graphName="amz", host="192.168.1.85:64803"))
		# print(ret.toJSON())

		for data_flow in ret:
			print(data_flow.toJSON())
		#     # print(12343566)
		#     with open('./node.csv', 'ab+') as f:
		#             data = data_flow.data
		#             f.write(data)

	def test_download_file(self):
		savePath = "./test_112.csv"
		ret = conn.download(ULTIPA_REQUEST.Download("amz_ids", 8, savePath),
							RequestConfig(graphName="amz"))
		# print(ret)
		# for data_flow in ret:
		# 	print(data_flow.toJSON())
