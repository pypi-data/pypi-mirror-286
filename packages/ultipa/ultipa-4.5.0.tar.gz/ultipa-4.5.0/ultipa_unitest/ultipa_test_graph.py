import time
import unittest

from ultipa import ULTIPA_REQUEST, ULTIPA
from ultipa.configuration.RequestConfig import RequestConfig
from ultipa.structs import DBType, GraphInfo
from ultipa.types.types_request import CommonSchema
from ultipa_unitest import conn


class TestUltipaMethods(unittest.TestCase):
	gname = 'ct_test_111'
	new_gname = 'ct_test123'

	str_name = 'name'
	int32_name = 'age'
	uint32_name = 'test_uint32'
	int64_name = 'test_int64'
	uint64_name = 'test_uint64'
	float_name = 'test_float'
	double_name = 'test_double'
	datetime_name = 'test_datetime'
	timestamp_name = 'test_timestamp'

	def test_listgraph(self):
		ret = conn.listGraph()
		# ret2 = conn.uql('show().graph(\"test_graph_ID\")')
		print(ret.toJSON())
		# print(ret.data[0].name)
		ret.Print()
		print(ret.data[0].name)

		# ret = conn.showGraph()
		# for i in ret.data:
		#     print(i.id,i.name,i.totalEdges,i.totalNodes)
		# ret1 = conn.uql('show().graph()')
		# print('>>>>', ret1.toJSON())
		# print('>>>>',ret.toJSON())

	def test_getgraph(self):
		ret = conn.getGraph(self.gname)
		# print(ret.data.id)
		# print(ret.data.name)
		# print(ret.data.totalEdges)
		# print(ret.data.totalNodes)

		print(ret.toJSON())
		ret.Print()

	def test_creategraph(self):
		ret = conn.createGraph(GraphInfo(graph=self.gname))
		print(ret.toJSON())
		# print(ret.data)
		# time.sleep(20)
		# property_list = [
		#     {'name': self.str_name, 'property_type': PropertyTypeStr.PROPERTY_LIST,"subTypes": [PropertyTypeStr.PROPERTY_STRING],'expect': True},
		# {'name': self.str_name, 'property_type': PropertyTypeStr.PROPERTY_STRING, 'expect': True},
		# {'name': self.int32_name, 'property_type': PropertyTypeStr.PROPERTY_INT, 'expect': True},
		# {'name': self.uint32_name, 'property_type': PropertyTypeStr.PROPERTY_UINT32, 'expect': True},
		# {'name': self.int64_name, 'property_type': PropertyTypeStr.PROPERTY_INT64, 'expect': True},
		# {'name': self.uint64_name, 'property_type': PropertyTypeStr.PROPERTY_UINT64, 'expect': True},
		# {'name': self.float_name, 'property_type': PropertyTypeStr.PROPERTY_FLOAT, 'expect': True},
		# {'name': self.double_name, 'property_type': PropertyTypeStr.PROPERTY_DOUBLE, 'expect': True},
		# {'name': self.datetime_name, 'property_type': PropertyTypeStr.PROPERTY_DATETIME,
		#  'expect': True},
		# {'name': self.timestamp_name, 'property_type': PropertyTypeStr.PROPERTY_TIMESTAMP,
		#  'expect': True}
		# ]
		# for pro in property_list:
		#     ret = conn.createProperty(
		#         ULTIPA_REQUEST.CreateProperty(type=DBType.DBNODE,
		#                                       commonSchema=CommonSchema(schema='default',
		#                                                               property=pro.get('name')),
		#                                       propertyType=pro.get('property_type'),subTypes=pro.get('subTypes')),
		#         RequestConfig(graphName="default"))
		#     print(ret.toJSON())

	def test_altergraph(self):
		ret = conn.alterGraph(oldGraphName="ct_test_111", newGraphName="ct_test_222")
		print(ret.toJSON(pretty=True))

	def test_dropgraph(self):
		ret = conn.dropGraph(graphName="ct_test_222")
		print(ret.toJSON(pretty=True))

	def test_graph_flow(self):
		graphName = "test12"
		ret = conn.showGraph()
		self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)

	def test_graph_flow1(self):
		ret = conn.showGraph()
		ret.Print()
		print(ret.toJSON())
		self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)

		ret = conn.dropGraph(GraphInfo(self.gname), RequestConfig(graphName=self.gname))
		print(ret.toJSON())
		print(ret.items)
		print(ret.status)
		print(ret.statistics)
		ret = conn.listGraph()
		self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)

		ret = conn.createGraph(GraphInfo(self.gname), RequestConfig(graphName=self.gname))
		print(ret.toJSON())
		self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)

		ret = conn.getGraph(self.gname, RequestConfig(graphName=self.gname))
		self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)

		ret = conn.alterGraph(ULTIPA_REQUEST.AlterGraph(self.gname, self.new_gname),
							  RequestConfig(graphName=self.gname))
		print(ret.toJSON())
		self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)

		ret = conn.alterGraph(ULTIPA_REQUEST.AlterGraph(self.new_gname, self.gname),
							  RequestConfig(graphName=self.gname))
		print(ret.toJSON())
		self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)

		ret = conn.dropGraph(self.gname, RequestConfig(graphName=self.gname))
		self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)

	#
	# #之前服务会挂掉
	# def test_creategraphAndInserdata(self):
	#     # ret = conn.createGraph(ULTIPA_REQUEST.Graph(self.gname),RequestConfig(graphSetName=self.gname))
	#     # print(ret.toJSON(pretty=True))
	#     ret = conn.createProperty(ULTIPA_REQUEST.CreatProperty(type=DBType.DBNODE, name='name'),RequestConfig(graphSetName=self.gname))
	#     print(ret.toJSON())
	#     ret = conn.createProperty(ULTIPA_REQUEST.CreatProperty(type=DBType.DBNODE, name='age',property_type=PropertyTypeStr.PROPERTY_INT),RequestConfig(graphSetName=self.gname))
	#     print(ret.toJSON())
	#     headers = [{"name": "name", "type": "PROPERTY_STRING"}, {"name": "age", "type": "PROPERTY_INT32"}, ]
	#     results = [{"name": "pytest1", "age": "20"}]
	#     graname = RequestConfig(graphSetName=self.gname)
	#     ret = conn.insertNodesBulk(ULTIPA_REQUEST.InsertNodeBulk(headers=headers, rows=results), graname)
	#     print(ret.toJSON())
	#
	#
	# def test_graphSet_flow(self):
	#     gname ='pytest2'
	#     ret = conn.dropGraph(ULTIPA_REQUEST.Graph(self.gname),RequestConfig(graphSetName=self.gname))
	#
	#     ret = conn.createGraph(ULTIPA_REQUEST.Graph(self.gname),RequestConfig(graphSetName=self.gname))
	#     print(ret.toJSON())
	#     self.assertEqual(ret.status.code,ULTIPA.Code.SUCCESS)
	#
	#     ret = conn.listGraph()
	#     print(ret.toJSON())
	#
	#     ret = conn.createProperty(ULTIPA_REQUEST.CreatProperty(type=DBType.DBNODE,name='name',property_type=PropertyTypeStr.PROPERTY_STRING),RequestConfig(graphSetName=self.gname))
	#     print(ret.toJSON())
	#     self.assertEqual(ret.status.code,ULTIPA.Code.SUCCESS)
	#
	#     ret = conn.createProperty(ULTIPA_REQUEST.CreatProperty(type=DBType.DBNODE,name='age',property_type=PropertyTypeStr.PROPERTY_INT),RequestConfig(graphSetName=self.gname))
	#     self.assertEqual(ret.status.code,ULTIPA.Code.SUCCESS)
	#
	#     headers = [{"name": "name", "type": "PROPERTY_STRING"}, {"name": "age", "type": "PROPERTY_INT32"}, ]
	#     results = [{"name": "pytest", "age": "20"}, {"name": "pytest1", "age": "22"}]
	#     ret = conn.insertNodesBulk(ULTIPA_REQUEST.InsertNodeBulk(headers=headers, rows=results),RequestConfig(graphSetName=self.gname))
	#     self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)
	#
	#     ret = conn.createProperty(ULTIPA_REQUEST.CreatProperty(type=DBType.DBEDGE, name='name',
	#                                                            property_type=PropertyTypeStr.PROPERTY_STRING),
	#                               RequestConfig(graphSetName=self.gname))
	#     self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)
	#
	#     ret = conn.createProperty(ULTIPA_REQUEST.CreatProperty(type=DBType.DBEDGE, name='rank',
	#                                                            property_type=PropertyTypeStr.PROPERTY_INT),
	#                               RequestConfig(graphSetName=self.gname))
	#     self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)
	#
	#     headers = [{"name": "name", "type": "PROPERTY_STRING"}]
	#     results = [{"from_id": 1, "to_id": 2, "name": "pytest"}, {"from_id": 1, "to_id": 8, "name": "pytest"},
	#                {"from_id": 2, "to_id": 8, "name": "pytest"}]
	#     ret = conn.insertEdgesBulk(ULTIPA_REQUEST.InsertEdgeBulk(headers=headers, rows=results), RequestConfig(graphSetName=self.gname))
	#     self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)
	#
	#
	# def test_yz(self):
	#     ret = conn.getGraph(ULTIPA_REQUEST.Graph(self.gname),RequestConfig(graphSetName=self.gname))
	#     print(ret.toJSON())
	#
	#     ret = conn.searchEdge(ULTIPA_REQUEST.SearchEdge(limit=10,select=['*']),RequestConfig(graphSetName=self.gname))
	#     print(ret.toJSON())
	#

	def test_mount(self):
		ret = conn.showGraph()
		ret.Print()
		self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)

		ret = conn.unmount(graph=self.gname)
		ret.Print()
		print(ret.toJSON())
		time.sleep(5)

		ret = conn.showGraph()
		ret.Print()
		ret = conn.mount(graph=self.gname)
		ret.Print()
		print(ret.toJSON())
		time.sleep(5)

		ret = conn.showGraph()
		ret.Print()
