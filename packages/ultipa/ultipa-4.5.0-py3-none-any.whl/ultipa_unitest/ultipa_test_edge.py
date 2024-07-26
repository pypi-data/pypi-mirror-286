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
        # 新插入的点通过ID 查询没有结果
        # ret = conn.searchEdge(ULTIPA_REQUEST.SearchEdge(filter=3387399,select=['name']),ULTIPA_REQUEST.Graph())
        # print(ret.toJSON())
        # self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)
        # ret = conn.searchEdge(ULTIPA_REQUEST.SearchMate(select=['name']))
        # self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)
        # ret = conn.searchEdge(ULTIPA_REQUEST.SearchMate())
        # self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)
        # ret = conn.searchEdge(ULTIPA_REQUEST.SearchEdge(select=[ULTIPA_REQUEST.UltipaReturn(ULTIPA_REQUEST.Schema('test'),'test',ULTIPA_REQUEST.UltipaEquation.avg,'eeee'),ULTIPA_REQUEST.UltipaReturn(ULTIPA_REQUEST.Schema('test'),'test',ULTIPA_REQUEST.UltipaEquation.sum,'eeee')],limit=10),RequestConfig())
        # print(ret.toJSON())
        # fi = FILTER.EqFilter(name='_from_id',value='1')
        # ret = conn.searchEdge(ULTIPA_REQUEST.SearchEdge(limit=10,select=['name','rank']),RequestConfig(graphSetName=self.gname))
        # for i in ret.data:
        #     print(i.values)

        # print(ret.toJSON())
        # self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)
        conn.defaultConfig.defaultGraph = self.gname
        # fi = ULTIPA_REQUEST.UltipaFilter(filterType=FilterEnum.EQ,property="name",value="test")
        ret = conn.searchEdge(ULTIPA_REQUEST.SearchEdge(select=ULTIPA_REQUEST.Return(alias="edges", allProperties=True, limit=10)))
        # ret = conn.searchEdge(
        #     ULTIPA_REQUEST.SearchEdge(select=ULTIPA_REQUEST.Return(aliasName="edges", all=True, limit=10)))
        print(ret.toJSON())
        # print(ret.data[0].asEdges()[0].values.get("date"))
        # print(ret.data[0].asEdges()[0].schema)

    # 4.0
    def test_insert(self):
        # insert().into(@name).edges([{'_from_u': 18, '_to_u': 19, 'name': 'Help1'}])
        conn.defaultConfig.defaultGraph = 'cloud_test1'
        # ret = conn.insertEdge(ULTIPA_REQUEST.InsertEdge(edges=[{'_from_uuid': 1, '_to_uuid': 2}], schemaName="default",isReturnID=True))
        ret = conn.insertEdge(ULTIPA_REQUEST.InsertEdge(edges=[{'_uuid':1,'_from_uuid': 1, '_to_uuid': 2,'name':'test1'}],upsert=True, schema="default",isReturnID=True))
        # ret = conn.insertEdge(ULTIPA_REQUEST.InsertEdge(edges=[{'_uuid':1,'_from_uuid': 1, '_to_uuid': 2,'name':'test1'}],overwrite=True, schemaName="default",isReturnID=True))
        print(ret.toJSON())
        # self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)

    def test_insert_bulk(self):

        # headers = [{"name": "test_int64", "type": "PROPERTY_INT64"}]
        results = [{'_from_uuid': 1, '_to_uuid': 2,'name':'test1'}]
        ret = conn.insertEdgesBulk(ULTIPA_REQUEST.InsertEdgeBulk(schema="default",rows=results,insertType=ULTIPA.InsertType.NORMAL), RequestConfig('cloud_test1'))
        print(ret.toJSON())

        # headers = [{"name": self.int64_name, "type": "PROPERTY_INT64"}]
        # results = [{'_from_id': 10, '_to_id': 12, headers[0].get('name'): vlist.get('value')}]
        # ret = self.conn.insertEdgesBulk(ULTIPA_REQUEST.InsertEdgeBulk(headers=headers, rows=results))
        # self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)

    def test_insert_bulk_o(self):
        # headers = [{"name": "test_int64", "type": "PROPERTY_INT64"}]
        results = [{"_from_o": 'ULTIPA8000000000000001', "_to_o": 'ULTIPA8000000000000002', 'name': 'test_o'}]
        ret = conn.insertEdgesBulk(ULTIPA_REQUEST.InsertEdgeBulk(rows=results), RequestConfig(self.gname))
        print(ret.toJSON())

    # 4.0
    def test_update(self):
        # ret = conn.updateEdge(ULTIPA_REQUEST.UpdateEdge(id=1, values={'rank': 30}),
        #                       RequestConfig("cloud_test1"))
        filter = ULTIPA_REQUEST.UltipaFilter(filterType=FilterEnum.EQ, property='rank', value=2,
                                             schema='default')
        ret = conn.updateEdge(ULTIPA_REQUEST.UpdateEdge(filter=filter, values={'rank': 12}),
                              RequestConfig("cloud_test1"))
        print(ret.toJSON())
        # self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)
        # ret = conn.updateEdge(ULTIPA_REQUEST.UpdateEdge(filter={'rank':{'$bt':[30,35]}}, values={'rank': 30}),RequestConfig())
        # self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)

    # 4.0
    def test_delete(self):

        # ret = conn.deleteEdge(ULTIPA_REQUEST.DeleteEdge(id=1))
        filter = ULTIPA_REQUEST.UltipaFilter(filterType=FilterEnum.BTE, property='test', value=1,
                                             schema='test')
        ret = conn.deleteEdge(ULTIPA_REQUEST.DeleteEdge(filter=filter), RequestConfig())
        print(ret.toJSON())
        # self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)


    def test_insert_edges(self):
        ret = conn.getGraph(ULTIPA_REQUEST.GraphInfo("test_edge"))
        print(ret.toJSON())
        if ret.status.code!=ULTIPA.Code.SUCCESS:
            ret  = conn.createGraph(ULTIPA_REQUEST.GraphInfo("test_edge"))
            assert  ret.status.code == ULTIPA.Code.SUCCESS
            conn.defaultConfig.defaultGraph='test_edge'
            ret = conn.createProperty(ULTIPA_REQUEST.CreateProperty(DBType.DBNODE,ULTIPA_REQUEST.CommonSchema(schema="default",property="name")))
            assert  ret.status.code == ULTIPA.Code.SUCCESS

        results = [{"schema":"default","values":[{"name": 'test_insert1'}]}]

        ret = conn.insertNodesBulk(ULTIPA_REQUEST.InsertEdgeBulk(rows=results,schema='test_edge',insertType=ULTIPA.InsertType.UPSERT),
                                   RequestConfig(graphName="test_edge"))
        print(ret.toJSON())

    def test_insert_InsertEdgesBatch(self):
        conn.defaultConfig.defaultGraph="ct_test"
        schema = [ULTIPA_REQUEST.Schema("default",
                                  [
                                    # ULTIPA_REQUEST.Property("id",ULTIPA.PropertyType.PROPERTY_ID),
                                    ULTIPA_REQUEST.Property("name",ULTIPA.PropertyType.PROPERTY_STRING),
                                    ULTIPA_REQUEST.Property("rank",ULTIPA.PropertyType.PROPERTY_INT32)
                                  ]
                                  )]
        rows = [ULTIPA.Edge(schema_name="default",values={"name":"aaa2","rank":1},from_uuid=1),ULTIPA.Edge(schema_name="default",values={"name":"aaa2","rank":2},from_uuid=2,to_uuid=1)]
        ret= conn.InsertEdgesBatch(InsertEdgeTable(schema,rows),InsertConfig(ULTIPA.InsertType.UPSERT))
        print(ret.toJSON())

    def test_insert_edge_bySchema(self):
        conn.defaultConfig.defaultGraph="ct_test"
        schema = ULTIPA_REQUEST.Schema("default",
                                  [
                                    # ULTIPA_REQUEST.Property("id",ULTIPA.PropertyType.PROPERTY_ID),
                                    ULTIPA_REQUEST.Property("name",ULTIPA.PropertyType.PROPERTY_STRING),
                                    ULTIPA_REQUEST.Property("rank",ULTIPA.PropertyType.PROPERTY_INT32)
                                  ]
                                  )
        rows = [ULTIPA.Edge({"name":"aaa2","rank":1},from_uuid=1,to_uuid=2),ULTIPA.Edge({"name":"aaa2","rank":2},from_uuid=2,to_uuid=1)]
        ret= conn.insertEdgesBatchBySchema(schema,rows,InsertConfig(ULTIPA.InsertType.UPSERT))
        print(ret.toJSON())

    def test_insert_edge_bySchema_list(self):
        conn.defaultConfig.defaultGraph="default"
        schema = ULTIPA_REQUEST.Schema("default",
                                  [
                                    ULTIPA_REQUEST.Property("name", ULTIPA.PropertyType.PROPERTY_LIST,subTypes=[ULTIPA.PropertyType.PROPERTY_STRING]),
                                  ]
                                  )
        rows = [ULTIPA.EntityRow({"name":["1asdas","asdfasdf"]},from_uuid=1,to_uuid=1)]
        ret= conn.insertEdgesBatchBySchema(schema,rows,InsertConfig(ULTIPA.InsertType.UPSERT))
        print(ret.toJSON())

    def test_InsertEdgesBatchAuto(self):
        conn.defaultConfig.defaultGraph = "ct_test"
        rows = [ULTIPA.Edge({"name": "aaa2", "rank": 1}, from_uuid=1, to_uuid=2,schema_name="default"),
                ULTIPA.Edge({"name": "aaa2", "rank": 2}, from_uuid=2, to_uuid=1,schema_name="default")]
        ret = conn.InsertEdgesBatchAuto(rows, InsertConfig(ULTIPA.InsertType.UPSERT))
        print(ret[0].toJSON())

    def test_time(self):
        ret = conn.searchEdge(ULTIPA_REQUEST.SearchEdge(select=ULTIPA_REQUEST.Return(alias="edges", allProperties=True, limit=100)), RequestConfig(graphName='amz'))
        print(ret.toJSON())
        print(ret.alias("edges").asEdges())


    def test_insert_edge_by_uql(self):
        conn.defaultConfig.defaultGraph="default"
        uql = "insert().into(@default).edges([{_from_uuid:1,_to_uuid:1,name:['asdfasdf','aasdfasdf']}])"
        ret = conn.uql(uql)
        print(ret.toJSON())

    def test_find_edge_by_uql(self):
        conn.defaultConfig.defaultGraph="default"
        uql = "find().edges() as e limit 100 return e{*}"
        ret= conn.uql(uql)
        print(ret.toJSON())
        ret.Print()

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
             doublename: None, timename: None},from_uuid=1,to_uuid=2)]
        ret = conn.insertEdgesBatchBySchema(schema, rows, InsertConfig(ULTIPA.InsertType.UPSERT))
        conn.batchInsertNodesBulk()
        print(ret.toJSON())

    def test_find_edges_null(self):
        conn.defaultConfig.defaultGraph = "pytest"
        ret = conn.uql("find().edges({@test}) return edges{*}")
        print(ret.toJSON())
