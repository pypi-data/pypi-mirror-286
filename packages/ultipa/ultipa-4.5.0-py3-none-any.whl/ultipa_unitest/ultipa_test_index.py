import unittest
from ultipa import *
from ultipa import Connection,ULTIPA_REQUEST,ULTIPA
from ultipa_unitest.helper import GetTestConnection
from ultipa_unitest import conn
class TestUltipaMethods(unittest.TestCase):
    graphName ='ct_test'

    def test_createIndex(self):
        conn.defaultConfig.defaultGraph=self.graphName
        ret = conn.createIndex(ULTIPA_REQUEST.CreateIndex(type=DBType.DBNODE,schema='default',property='name'))
        # ret = conn.createIndex(ULTIPA_REQUEST.CreatIndex(DBtype=DBType.DBEDGE,schemaName='test',propertyName='test_str'))
        print(ret.toJSON())
        print(ret.data)

    def test_createFulltext(self):
        conn.defaultConfig.defaultGraph=self.graphName
        # ret = conn.createFulltext(ULTIPA_REQUEST.CreatFulltext(DBtype=DBType.DBNODE,schemaName='test',propertyName='test_str',name='testNodeFulltext'))
        ret = conn.createFulltext(ULTIPA_REQUEST.CreateFulltext(type=DBType.DBEDGE,schema='test',property='test_str',name='testEdgeFulltext'))
        print(ret.toJSON())



    def test_showIndex(self):
        conn.defaultConfig.defaultGraph = "default"
        # ret = conn.showIndex()

        # ret = conn.showIndex(request=ULTIPA_REQUEST.ShowIndex(DBtype=DBType.DBNODE),requestConfig=RequestConfig(graphSetName=self.graphName))
        ret = conn.showIndex(request=ULTIPA_REQUEST.ShowIndex(type=DBType.DBNODE))
        # ret = conn.showIndex()
        print(ret.data[0].name)
        print(ret.data[0])
        print(ret.toJSON())

    def test_fulltext(self):
        conn.defaultConfig.defaultGraph = "miniCircle"
        ret = conn.showFulltext()
        ret_1 = ret.alias("_nodeFulltext").asTable().toDicts()
        print(ret_1)
        # ret = conn.showFulltext(request=ULTIPA_REQUEST.ShowIndex(DBtype=DBType.DBNODE))
        # ret = conn.showFulltext(request=ULTIPA_REQUEST.ShowIndex(DBtype=DBType.DBEDGE))
        print(ret.toJSON())

    def test_dropIndex(self):
        conn.defaultConfig.defaultGraph=self.graphName
        # ret = conn.dropIndex(ULTIPA_REQUEST.DropIndex(DBType.DBNODE,'test','test_str'))
        ret = conn.dropIndex(ULTIPA_REQUEST.DropIndex(type=DBType.DBEDGE,schema='test',property='test_str'))
        print(ret.toJSON())

    def test_dropFulltext(self):
        conn.defaultConfig.defaultGraph = self.graphName
        # ret = conn.dropFulltext(ULTIPA_REQUEST.DropFulltext(DBType.DBNODE,'testNodeFulltext'))
        ret = conn.dropFulltext(ULTIPA_REQUEST.DropFulltext(type=DBType.DBEDGE,name='testEdgeFulltext'))
        print(ret.toJSON())

    def test_index_flow(self):
        conn.defaultConfig.defaultGraph = self.graphName
        ret = conn.createIndex(ULTIPA_REQUEST.CreateIndex(type=DBType.DBNODE, schema='default', property='name'))
        print(ret.toJSON())
        print(ret.items)
        ret = conn.showIndex(request=ULTIPA_REQUEST.ShowIndex(type=DBType.DBNODE))
        print(ret.data[0].name)
        print(ret.data[0].properties)
        print(ret.data[0].status)
        print(ret.data[0].schema)
        print(ret.toJSON())
        ret.Print()

        ret = conn.dropIndex(ULTIPA_REQUEST.DropIndex(type=DBType.DBNODE, schema='default', property='name'))
        print(ret.toJSON())

        ret = conn.createFulltext(ULTIPA_REQUEST.CreateFulltext(type=DBType.DBNODE, schema='default', property='name',name="test_name"))
        print(ret.toJSON())
        ret.Print()

        ret = conn.createFulltext(ULTIPA_REQUEST.CreateFulltext(type=DBType.DBEDGE, schema='default', property='name',name="test_edge_name"))
        print(ret.toJSON())
        ret.Print()

        ret = conn.showFulltext()
        print(ret.toJSON())
        ret.Print()


        ret = conn.dropFulltext(ULTIPA_REQUEST.DropFulltext(type=DBType.DBNODE,name='test_name'))
        print(ret.toJSON())
        print(ret.items)

        ret = conn.dropFulltext(ULTIPA_REQUEST.DropFulltext(type=DBType.DBEDGE,name='test_edge_name'))
        print(ret.toJSON())











