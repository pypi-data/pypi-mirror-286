import csv
import datetime
import json
import random
import time
import unittest
from datetime import date
from ultipa import Connection, ULTIPA_REQUEST, ULTIPA, FILTER, InsertNode, Schema
from ultipa.configuration.InsertConfig import InsertConfig
from ultipa.configuration.RequestConfig import RequestConfig
from ultipa.structs import InsertType, Property, DBType, Schema, PropertyTypeStr, PropertyType, GraphInfo
from ultipa.utils.ufilter.new_ufilter import FilterEnum
from ultipa_unitest import conn


class TestUltipaMethods(unittest.TestCase):
	gname = 'default'

	def test(self):
		ret = conn.test()
		print(ret)

	# 4.0
	def test_search(self):
		# conn.test()
		# ret = conn.searchNode(ULTIPA_REQUEST.SearchNode(select=[ULTIPA_REQUEST.UltipaReturn(ULTIPA_REQUEST.Schema('test'),'test'),ULTIPA_REQUEST.UltipaReturn(ULTIPA_REQUEST.Schema('test'),'test',ULTIPA_REQUEST.UltipaEquation.sum,'eeee')],limit=10),RequestConfig())
		# ret = conn.searchNode(ULTIPA_REQUEST.SearchNode(select=[ULTIPA_REQUEST.UltipaReturn('test','test',ULTIPA_REQUEST.UltipaEquation.count,['eeee']),ULTIPA_REQUEST.UltipaReturn('test','test',ULTIPA_REQUEST.UltipaEquation.sum,['eeee'])],limit=10),RequestConfig())
		conn.defaultConfig.defaultGraph = self.gname
		# ret = conn.searchNode(ULTIPA_REQUEST.SearchNode(select=ULTIPA_REQUEST.Return(aliasName="nodes",all=True,limit=100)))
		# print(ret.toJSON())
		# print(ret.data[0].asNodes()[0].schema)
		# ret = conn.searchNode(ULTIPA_REQUEST.SearchNode(ULTIPA_REQUEST.Return(aliasName="nodes",all=True,limit=100)))
		# print(ret.toJSON())

		# filter = ULTIPA_REQUEST.UltipaFilter(
		#     schemaName='default', filterType=FilterEnum.BT, propertyName='test', value=[])
		#
		# # value1 = vlist.get('value1')
		# # value2 = vlist.get('value2')
		# filter1 = ULTIPA_REQUEST.UltipaFilter(
		#     schemaName='default', filterType=FilterEnum.LTE, propertyName='test',
		#     value='test')
		# filter2 = ULTIPA_REQUEST.UltipaFilter(
		#     schemaName='default', filterType=FilterEnum.EQ, propertyName='test',
		#     value='test')
		# fileter3 = ULTIPA_REQUEST.UltipaAndFilter([filter1,filter2])
		# #
		# # ret = conn.searchNode(
		# #     ULTIPA_REQUEST.SearchNode(select=ULTIPA_REQUEST.Return(aliasName="ed", all=True, limit=100),filter=fileter3))
		# ret = conn.deleteNode(ULTIPA_REQUEST.DeleteNode(filter=fileter3))
		# print(ret.toJSON())

		# print(ret.data[0].asNodes()[0].schema)
		filter = ULTIPA_REQUEST.UltipaFilter(
			schema='default', filterType=FilterEnum.EQ, property='name', value="test1")
		ret = conn.searchNode(
			ULTIPA_REQUEST.SearchNode(ULTIPA_REQUEST.Return(alias="nodes", allProperties=True, limit=100),
									  filter=filter))
		print(ret.toJSON())

	def test_insert(self):
		# conn.defaultConfig.defaultGraph="default"
		# ret = conn.insertNode(ULTIPA_REQUEST.InsertNode(nodes=[{'name':'test'}],schemaName="default"),RequestConfig(graphSetName="cloud_test1"))
		# ret = conn.insertNode(ULTIPA_REQUEST.InsertNode(nodes=[{'name':'test'}],schemaName="default"),RequestConfig(graphSetName="cloud_test1"))
		# ret = conn.insertNode(ULTIPA_REQUEST.InsertNode(nodes=[{'_uuid':1,'name':'test2'}],schemaName="default",upsert=True),RequestConfig(graphSetName="cloud_test1"))
		ret = conn.insertNode(InsertNode(nodes=[{'decimal': 1.1}], schema="default"),
							  RequestConfig(graphName="default"))
		# ret = conn.getRaftLeader()

		print(ret.toJSON())

	# def test_insert_bulk_check_o(self):
	#     conn.createProperty(request=ULTIPA_REQUEST.CreateProperty(type=DBType.DBNODE,commonSchema=ULTIPA_REQUEST.CommonSchema('default','name')))
	#     results = [{"schema":"default","values":[{"name": 'test_insert1','age':1},{"name": 'test_insert12'},{"name": 'test_insert1'},{"name": 'test_insert12'}]}]
	#     # conn.defaultConfig.defaultGraph='pythonInsertNode'
	#     ret = conn.insertNodesBulk(ULTIPA_REQUEST.InsertNodeBulk(schema="default",rows=results,insertType=ULTIPA.InsertType.UPSERT),RequestConfig())
	#     print(ret.toJSON())

	def test_insert_bulk(self):
		conn.defaultConfig.defaultGraph = 'default'
		results = [{"decimal": "1.1"}]
		# ret = conn.insertNodesBatchAuto(
		# 	ULTIPA_REQUEST.InsertNodeBulk(schema="default", rows=results, insertType=ULTIPA_REQUEST.InsertType.UPSERT))

		ret = conn.insertNodesBatchAuto(nodes=[ULTIPA.EntityRow(schema="default",
																values={"decimal": 1.1})],
										config=InsertConfig(insertType=ULTIPA_REQUEST.InsertType.NORMAL,
															graphName='default'))

		print(ret.toJSON())

	# 4.0
	def test_update(self):
		# ret = conn.updateNode(ULTIPA_REQUEST.UpdateNode(id=1, values={'age': 1}),
		#                       RequestConfig(graphSetName='cloud_test1'))
		# print(ret.toJSON())

		filter = ULTIPA_REQUEST.UltipaFilter(filterType=FilterEnum.EQ, property='age', value=2,
											 schema='default')
		ret = conn.updateNode(ULTIPA_REQUEST.UpdateNode(filter=filter, values={'age': 5}),
							  RequestConfig(graphName='cloud_test1'))
		print(ret.toJSON())

	# self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)
	# ret = conn.updateNode(ULTIPA_REQUEST.UpdateMate(filter={'age':{'$bt':[30,35]}},params={'age':30}))
	# self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)

	# 4.0
	def test_delete(self):
		# ret = conn.deleteNode(ULTIPA_REQUEST.DeleteNode(id=4),
		#                       RequestConfig(graphSetName=self.gname))

		filter = ULTIPA_REQUEST.UltipaFilter(filterType=FilterEnum.EQ, property='name',
											 value="aaa2aaa2aaa2aaa2aaa2aaa2aaa2aaa2aaa2aaa2aaa2aaa2aaa2aaa2aaa2aaa2",
											 schema='default')
		ret = conn.deleteNode(ULTIPA_REQUEST.DeleteNode(uuid=1),
							  RequestConfig(graphName=self.gname))
		print(ret.toJSON())

	# self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)

	# 4.0
	def test_insert_flow(self):
		strname = 'test'
		int32name = 'test_int'
		uint32name = 'test_uint32'
		int64name = 'test_int64'
		uint64name = 'test_uint64'
		floatname = 'test_float'
		doublename = 'test_double'

		ret = conn.insertNode(ULTIPA_REQUEST.InsertNode(nodes=[
			{strname: 'test', int32name: -1, uint32name: -4294967295, int64name: 2133435, uint64name: -12345666,
			 floatname: 0.1234567, doublename: 0.123456789101112}], schema='test'),
			RequestConfig(graphName=self.gname))
		print(ret.toJSON())

	def test_time(self):
		# ret = conn.createProperty(ULTIPA_REQUEST.CreateProperty(type=DBType.DBNODE, name='node_time',
		#                                                        property_type=PropertyTypeStr.PROPERTY_DATETIME),
		#                           RequestConfig(self.gname))
		# print(ret.toJSON())
		# self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)
		ret = conn.searchNode(
			ULTIPA_REQUEST.SearchNode(select=ULTIPA_REQUEST.Return(alias="nodes", allProperties=True, limit=100)),
			RequestConfig(graphName='amz'))
		print(ret.toJSON())
		print(ret.alias("nodes").asNodes())
		ret.Print()

	# results = [{'name':'test',"node_time": '2021-03-09 14:46:50.906778'}]
	# ret = conn.insertNodesBulk(ULTIPA_REQUEST.InsertNodeBulk(rows=results),
	#                            RequestConfig(graphName=self.gname))
	# print(ret.toJSON())

	# propertyRet = conn.uql('show().node_property()')
	# print(propertyRet.toJSON())
	# conn.defaultConfig.defaultGraph='test_datetime'
	# request = ULTIPA_REQUEST.SearchNode(limit=-1,select=['*'], filter=FILTER.LteFilter('test_time',"2021-03-09 14:46:50.906778"))
	# ret = conn.searchNode(request)
	# print(ret.toJSON())

	# request = ULTIPA_REQUEST.SearchNode(limit=-1, select=['*'],
	#                                     filter=FILTER.NinFilter('test_time', ["2021-03-09 14:46:50.906778","2021-03-09 14:46:50.906778"]))
	# ret = conn.searchNode(request)
	# print(ret.toJSON())

	def test_find_nodes(self):
		conn.defaultConfig.defaultGraph = 'test_edge_create7699'
		ret = conn.searchNode(
			ULTIPA_REQUEST.SearchNode(select=ULTIPA_REQUEST.Return(alias="nodes", allProperties=True, limit=10)))
		print(ret.toJSON())
		ret.Print()

	# ret = conn.uql("find().nodes(116) return nodes{*}")
	# print(ret.toJSON())
	# ret = conn.uql("find().nodes(116) return nodes{*}")
	# print(ret.toJSON())

	def test_find_nodes_array(self):
		conn.defaultConfig.defaultGraph = 'default'
		ret = conn.uql("find().nodes() as nodes return collect(distinct(nodes)) as arrNode")
		print(ret.toJSON())
		ret.Print()

	def test_nodes(self):
		# results = [{"schema":"default","values":[{"_id": '1'}]}]
		# ret = conn.insertNodesBulk(ULTIPA_REQUEST.InsertNodeBulk(rows=results,graph_name='default',insert_type=ULTIPA.InsertType.UPSERT))
		conn.defaultConfig.defaultGraph = 'test_node'
		ret = conn.uql("insert().into(@default).nodes([{'age': 101}])")
		print(ret.toJSON())

	def test_insert_nodes(self):
		# ret = conn.getGraph(ULTIPA_REQUEST.Graph("test_node"))
		# print(ret.toJSON())
		# if ret.status.code!=ULTIPA.Code.SUCCESS:
		#     ret  = conn.createGraph(ULTIPA_REQUEST.CreateGraph("test_node"))
		#     assert  ret.status.code == ULTIPA.Code.SUCCESS
		#     conn.defaultConfig.defaultGraph='test_node'
		#     ret = conn.createProperty(ULTIPA_REQUEST.CreateProperty(DBType.DBNODE,ULTIPA_REQUEST.CommonSchema(schemaName="default",propertyName="name")))
		#     assert  ret.status.code == ULTIPA.Code.SUCCESS

		results = [{"schema": "default",
					"values": [{"name": 'test_insert1', "age": 1}, {"name": 'test_insert1', "age": 1},
							   {"name": 'test_insert1', "age": 1}, {"name": 'test_insert1', "age": 1},
							   {"name": 'test_insert1', "age": 1}]}]

		ret = conn.insertNodesBulk(
			ULTIPA_REQUEST.InsertNodeBulk(schema="default", rows=results, insertType=ULTIPA.InsertType.UPSERT),
			RequestConfig(graphName="test_node"))
		print(ret.toJSON())

	#
	# results_edge = [{"schema":"default","values":[{"_from_uuid": 1,"_to_uuid":2}]}]
	#
	# ret = conn.insertEdgesBulk(ULTIPA_REQUEST.InsertEdgeBulk(rows=results_edge,insert_type=ULTIPA.InsertType.UPSERT),
	#                            RequestConfig(graphName="test_node"))
	# print(ret.toJSON())

	def get_vales(self, j):
		return [{"schema": "default", "values": [{"name": f'test_insert{j}{i}'}]} for i in range(1000)]

	def test_insert_node(self):

		for j in range(5):
			results = self.get_vales(j)
			print(results)
			print(j, 'begin', len(results))
			ret = conn.insertNodesBulk(
				ULTIPA_REQUEST.InsertNodeBulk(schema="default", rows=results, insertType=ULTIPA.InsertType.UPSERT),
				RequestConfig(graphName="default"))
			print(ret.toJSON())

	# print(j,'end',len(ret.data.uuids))
	# if j==4:
	#     results= [{"schema": "default","values":[{"name": f'test_insert{j}{i}'}]} for i in range(random.randint(500,1000))]
	#     ret = conn.insertNodesBulk(
	#         ULTIPA_REQUEST.InsertNodeBulk(rows=results,insertType=ULTIPA.InsertType.UPSERT),
	#         RequestConfig(graphName="test_node"))
	#     print(ret.toJSON())
	#     print(j, 'end', len(ret.data.uuids))

	def test_export_node(self):
		ret = conn.export(
			ULTIPA_REQUEST.Export(DBType.DBNODE, limit=10, schema="Company", properties=['_id', "type", "name"]),
			requestConfig=RequestConfig(graphName='gate'))
		print(ret.data[0].getProperty())

	def test_truncate(self):
		ret = conn.truncate(
			ULTIPA_REQUEST.Truncate(graph=self.gname, schema="default", truncateType=ULTIPA.TruncateType.NODES))
		print(ret.toJSON())

	def test_truncate_all(self):
		ret = conn.truncate(ULTIPA_REQUEST.Truncate(graph=self.gname, allData=True))
		print(ret.toJSON())

	def test_compact(self):
		ret = conn.compact("default")
		print(ret.toJSON())

	def test_insert_NodesBatch(self):
		conn.defaultConfig.defaultGraph = "ct_test"

		# schema = ULTIPA_REQUEST.Schema("default",
		#                                [
		#                                    # ULTIPA_REQUEST.Property("id",ULTIPA.PropertyType.PROPERTY_ID),
		#                                    ULTIPA_REQUEST.Property("name", ULTIPA.PropertyType.PROPERTY_STRING),
		#                                    ULTIPA_REQUEST.Property("age", ULTIPA.PropertyType.PROPERTY_INT32)]
		#                                )
		schema = [ULTIPA_REQUEST.Schema("default",
										[
											# ULTIPA_REQUEST.Property("id",ULTIPA.PropertyType.PROPERTY_ID),
											Property("name", ULTIPA.PropertyType.PROPERTY_STRING)
										]
										)]
		rows = [ULTIPA.Node(schema_name="default", values={"name": "aaa2"})]
		ret = conn.InsertNodesBatch(ULTIPA_REQUEST.InsertNodeTable(schema, rows),
									InsertConfig(ULTIPA.InsertType.UPSERT))
		print(ret.toJSON())

	def test_insert_node_bySchema(self):
		conn.defaultConfig.defaultGraph = "default"
		schema = ULTIPA_REQUEST.Schema("default",properties=[
										   Property("decimal", ULTIPA.PropertyType.PROPERTY_DECIMAL),
									   ],dbType=DBType.DBNODE)
		rows = [ULTIPA.EntityRow({"decimal": 1.1})]
		ret = conn.insertNodesBatchBySchema(schema, rows, InsertConfig(ULTIPA_REQUEST.InsertType.UPSERT))
		print(ret.toJSON())

	def test_insert_node_bySchema_list(self):
		conn.defaultConfig.defaultGraph = "default"
		schema = Schema(name="default", dbType=DBType.DBNODE,properties=[Property("test_set", ULTIPA.PropertyType.PROPERTY_LIST, subTypes=[ULTIPA.PropertyType.PROPERTY_STRING])]
						)
		rows = [ULTIPA.EntityRow(
			{"test_set": ["aaa2aaa2aaa2aaa2aaa2aaa2aaa2aaa2aaa2aaa2aaa2aaa2aaa2aaa2aaa2aaa2", "asdfasdfasdfasdfasdf"]})]
		ret = conn.insertNodesBatchBySchema(schema, rows, InsertConfig(InsertType.UPSERT))
		print(ret.toJSON())


	def test_insert_node_bySchema_set(self):
		conn.defaultConfig.defaultGraph = "default"
		schema = Schema(name="test_set", dbType=DBType.DBNODE,properties=[
			Property("test_set", ULTIPA.PropertyType.PROPERTY_SET, subTypes=[ULTIPA.PropertyType.PROPERTY_STRING]),
		]
						)

		rows = [ULTIPA.EntityRow(
			{"test_set": {"1", "1", "2", "3"}})]
		ret = conn.insertNodesBatchBySchema(schema, rows, InsertConfig(InsertType.UPSERT))
		print(ret.toJSON())

	def test_insert_node_bySchema_list_Null(self):
		conn.defaultConfig.defaultGraph = "pythonSdkInsert"
		schema = ULTIPA_REQUEST.Schema("insertNode",None,properties=
									   [
										   Property("typeListString", ULTIPA.PropertyType.PROPERTY_LIST,subTypes=[ULTIPA.PropertyType.PROPERTY_STRING]),
									   ]
									   )
		rows = [ULTIPA.EntityRow({"typeListString": None})]
		conn.defaultConfig.defaultGraph = "gosdk"
		schema = ULTIPA_REQUEST.Schema("testTimeZone", dbType=DBType.DBNODE

		[
			Property("typeTimestamp", type=PropertyTypeStr.PROPERTY_TIMESTAMP),
		]
									   )
		rows = [ULTIPA.EntityRow({"typeTimestamp": "2023-8-4 15:00:00"})]
		conn.defaultConfig.defaultGraph = "test"
		rows = [
			ULTIPA.Node({"name": "sfldsjflks","type": "222",}, schema_name="person",id="ULTIPA800000000000000C"),
			ULTIPA.Node({"_isEnd": "true"}, schema_name="agent",id="ULTIPA800000000000000C"),
			ULTIPA.Node({ "name": "常九", "type": "666",}, schema_name="person",id="ULTIPA8000000000000009"),
			ULTIPA.Node({"name": "sfldsjflks","type": "222",}, schema_name="person"),
			ULTIPA.Node({"name": "sfldsjflks","type": "222",}, schema_name="person")
				]
		ret = conn.insertNodesBatchAuto(rows, InsertConfig(InsertType.UPSERT))
		for i in ret:
			print(i.toJSON())

	def test_InsertNodesBatchAuto_JSON(self):
		conn.defaultConfig.defaultGraph = "test"
		ret = open("../path.json", "r")
		dataRet = json.loads(ret.read())
		# print(dataRet.get("data"))
		nodeRow = []
		edgeRow = []
		for node in dataRet["data"]["nodes"]:
			nodeRow.append(ULTIPA.Node(node.get("values"), schema_name=node.get("schema"), id=node.get("_id")))

		for edge in dataRet["data"]["edges"]:
			edgeRow.append(ULTIPA.Edge(edge.get("values"), schema_name=edge.get("schema"),from_id=edge.get("_from_id"),to_id=edge.get("_to_id")))
		# rows = [
		# 	ULTIPA.Node({"name": "sfldsjflks", "type": "222", }, schema_name="person", id="ULTIPA800000000000000C"),
		# 	ULTIPA.Node({"_isEnd": "true"}, schema_name="agent", id="ULTIPA800000000000000C"),
		# 	ULTIPA.Node({"name": "常九", "type": "666", }, schema_name="person", id="ULTIPA8000000000000009"),
		# 	ULTIPA.Node({"name": "sfldsjflks", "type": "222", }, schema_name="person"),
		# 	ULTIPA.Node({"name": "sfldsjflks", "type": "222", }, schema_name="person")
		# ]
		#
		# ret = conn.insertNodesBatchAuto(rows, InsertConfig(InsertType.UPSERT))
		# for i in ret:
		# 	print(i.toJSON())
		print(nodeRow)
		print(edgeRow)


	def test_insertByCSV(self):
		# conn.defaultConfig.defaultGraph = "ct_test"
		ret = conn.createGraph(GraphInfo(graph="ct_test"))
		rows = []
		propertyType = []
		properties = []
		type = []
		with open("../data/nodes.csv", "r", encoding="utf-8-sig") as csvfile:
			reader = csv.reader(csvfile)
			# 这里不需要readlines
			for i, line in enumerate(reader):
				if i == 0:
					for i, property in enumerate(line):
						k1, k2 = property.split(":")
						propertyType.append({k1: k2})
						type.append({"index": i, "type": k2})
						properties.append(k1)
					continue
				for i in type:
					if i.get("type") in ["int", "int32", "int64"]:
						if line[i.get("index")] == "":
							line[i.get("index")] = 0
							continue
						line[i.get("index")] = int(line[i.get("index")])
					if i.get("type") in ["float", "double"]:
						if line[i.get("index")] == "":
							line[i.get("index")] = 0.0
							continue
						line[i.get("index")] = float(line[i.get("index")])
				print(dict(zip(properties, line)))

		# id = line.get("_id")
		# line.__delitem__("_id")
		# rows.append(ULTIPA.Node(line, schema_name="test", uuid=int(id)))

	def test_insert_null(self):
		conn.defaultConfig.defaultGraph = "pytest"

		strname = 'test_str'
		int32name = 'test_int'
		uint32name = 'test_uint32'
		int64name = 'test_int64'
		uint64name = 'test_uint64'
		floatname = 'test_float'
		doublename = 'test_double'
		timename = 'test_DateTime'
		schema = ULTIPA_REQUEST.Schema("test",
									   [
										   ULTIPA_REQUEST.Property(strname, ULTIPA.PropertyType.PROPERTY_STRING),
										   ULTIPA_REQUEST.Property(int32name, ULTIPA.PropertyType.PROPERTY_INT32),
										   ULTIPA_REQUEST.Property(uint32name, ULTIPA.PropertyType.PROPERTY_UINT32),
										   ULTIPA_REQUEST.Property(int64name, ULTIPA.PropertyType.PROPERTY_INT64),
										   ULTIPA_REQUEST.Property(uint64name, ULTIPA.PropertyType.PROPERTY_UINT64),
										   ULTIPA_REQUEST.Property(floatname, ULTIPA.PropertyType.PROPERTY_FLOAT),
										   ULTIPA_REQUEST.Property(doublename, ULTIPA.PropertyType.PROPERTY_DOUBLE),
										   ULTIPA_REQUEST.Property(timename, ULTIPA.PropertyType.PROPERTY_DATETIME),
									   ]
									   )
		rows = [ULTIPA.EntityRow(
			{strname: None, int32name: None, uint32name: None, int64name: None, uint64name: None, floatname: None,
			 doublename: None, timename: None})]
		ret = conn.InsertNodesBatchBySchema(schema, rows, InsertConfig(ULTIPA.InsertType.UPSERT))
		print(ret.toJSON())

	def test_find_nodes_null(self):
		conn.defaultConfig.defaultGraph = "pytest"
		ret = conn.uql("find().nodes({@test}) return nodes{*}")
		print(ret.toJSON())
# schema = ULTIPA_REQUEST.Schema("test",
# 							   [
# 								   ULTIPA_REQUEST.Property("name", ULTIPA.PropertyType.PROPERTY_STRING),
# 								   ULTIPA_REQUEST.Property("nodeType", ULTIPA.PropertyType.PROPERTY_STRING),
# 								   ULTIPA_REQUEST.Property("rating", ULTIPA.PropertyType.PROPERTY_STRING),
# 								   ULTIPA_REQUEST.Property("type", ULTIPA.PropertyType.PROPERTY_STRING),
# 								   ULTIPA_REQUEST.Property("year", ULTIPA.PropertyType.PROPERTY_STRING),
# 								]
# 							   )
# ret = conn.InsertNodesBatchBySchema(schema, rows, InsertConfig(ULTIPA.InsertType.UPSERT))
# print(ret.toJSON())
# ret = conn.InsertNodesBatchAuto(rows, InsertConfig(ULTIPA.InsertType.NORMAL))
# for i in ret:
# print(ret.toJSON())

# # 点文件里面 _id 或者 _uuid 或者不填写将会自动生成uuid 和 id
# ret = conn.InsertByCSV("../data/nodes.csv",DBType.DBNODE,InsertConfig(ULTIPA.InsertType.NORMAL),schemaName="test")
# print(ret.toJSON())
#
# # 边文件里面 必须包含 _from_id,_to_id 或者 _from_uuid,_to_uuid 这样才能保证边插入成功
# # ret = conn.InsertByCSV("../data/edges.csv",DBType.DBEDGE,InsertConfig(ULTIPA.InsertType.NORMAL),schemaName="test")
# # print(ret.toJSON())


	def test_insert_node_bySchema_1(self):
		conn.defaultConfig.defaultGraph = "pythonSdkInsert"
		schema = ULTIPA_REQUEST.Schema("insertNode", dbType=DBType.DBNODE,properties=

		[
			Property("typeTimestamp", type=PropertyType.PROPERTY_TIMESTAMP),
			Property("typeListTimestamp", type=PropertyType.PROPERTY_LIST,subTypes=[PropertyType.PROPERTY_TIMESTAMP]),
		]
									   )
		rows = [ULTIPA.EntityRow({"typeTimestamp": "2023-8-4 15:00:00","typeListTimestamp":["2023-8-4 15:00:00","2023-8-4 15:00:00"]})]
		ret = conn.insertNodesBatchBySchema(schema, rows, InsertConfig(InsertType.UPSERT,timeZone="America/Toronto"))
		print(ret.toJSON())


	def test_find_node_bySchema(self):
		conn.defaultConfig.defaultGraph = "pythonSdkInsert"
		uql = "find().nodes(5) as nodes return nodes{*}"
		ret = conn.uql(uql,requestConfig=RequestConfig(timeZone="America/Toronto"))
		# print(ret.toJSON())
		ret.Print()