import random
import unittest
from typing import List

from ultipa import ULTIPA_REQUEST, ULTIPA, Schema
from ultipa import FILTER
from ultipa.configuration.RequestConfig import RequestConfig
from ultipa.structs import GraphInfo
from ultipa.structs.DBType import DBType
from ultipa_unitest import conn


class TestUltipaMethods(unittest.TestCase):

    gname = 'miniCircle'

    def test_list(self):

        ret = conn.listSchema(requestConfig=RequestConfig(graphName=self.gname))
        # print(ret.data[0].data[0].type)
        # print(ret.data)
        print(ret.toJSON())
        ret.Print()

    def test_listNodeSchema(self):
        # conn.defaultConfig.defaultGraph = "ct_test"
        ret = conn.showSchema(dbType=DBType.DBNODE,schemaName="tetstssss")
        print(ret.toJSON())

    def test_listEdgeSchema(self):
        ret = conn.showSchema(ULTIPA_REQUEST.ShowSchema(type=DBType.DBEDGE))
        # print(ret.data.edgeSchemas)
        print(ret.toJSON())
        ret.Print()

    def test_getNodeSchema(self):
        ret = conn.showSchema(ULTIPA_REQUEST.ShowSchema(type=DBType.DBNODE,schema='default'))
        print(ret.toJSON())
        ret.Print()

    def test_getEdgeSchema(self):
        ret = conn.showSchema(ULTIPA_REQUEST.ShowSchema(type=DBType.DBEDGE,schema='default'))
        print(ret.toJSON())


    def test_createNodeSchema(self):
        conn.defaultConfig.defaultGraph="test_py"
        ret = conn.createSchema(ULTIPA_REQUEST.CreateSchema('test',DBType.DBNODE))
        print(ret.toJSON())
        # ret = conn.createSchema(ULTIPA_REQUEST.CreateSchema(schemaName="test",type=DBType.DBNODE,description="test"))
        # print(ret.toJSON())

    def test_creatEdgeSchema(self):
        conn.defaultConfig.defaultGraph="test_py"
        ret = conn.createSchema(ULTIPA_REQUEST.CreateSchema(name="test",type=DBType.DBEDGE,description="test"))
        print(ret.toJSON())

    def test_alter(self):
        # ret = conn.createSchema(ULTIPA_REQUEST.CreateSchema(schemaName="test",schemaType=DBType.DBNODE))
        ret = conn.alterSchema(ULTIPA_REQUEST.AlterSchema(schema='test',type=DBType.DBNODE,newDescription="test",newName='test1'))
        print(ret.toJSON())


    def test_drop(self):
        # ret = conn.createSchema(ULTIPA_REQUEST.CreateSchema(schemaName="test",schemaType=DBType.DBNODE))
        ret = conn.dropSchema(ULTIPA_REQUEST.DropSchema(schema='test',type=DBType.DBNODE))
        print(ret.toJSON())

    def test_schema_flow(self):
        conn.defaultConfig.defaultGraph = self.gname
        ret = conn.getGraph(self.gname, RequestConfig(graphName=self.gname))
        print(ret.toJSON())
        if not ret.data:
            ret = conn.createGraph(GraphInfo(self.gname), RequestConfig(graphName=self.gname))
            print(ret.toJSON())
            self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)

        ret = conn.createSchema(Schema('test_schema', DBType.DBNODE))
        print(ret.toJSON())
        self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)

        ret = conn.createSchema(Schema('test_schema', DBType.DBEDGE))
        print(ret.toJSON())
        self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)

        ret = conn.showSchema(dbType=DBType.DBNODE)
        print(ret.toJSON())
        # for i in ret.alias("_nodeSchema").asSchemas():
        #     print(i.name)
        #     print(i.properties)
        #     print(i.name)
        #     print(i.name)


        ret = conn.showSchema(dbType=DBType.DBEDGE)
        print(ret.toJSON())

        ret = conn.alterSchema(schemaName='test_schema', dbType=DBType.DBNODE,newSchemaName='test_schema_1', description="test")
        print(ret.toJSON())
        self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)

        ret = conn.alterSchema(schemaName='test_schema', dbType=DBType.DBEDGE, newSchemaName='test_schema_1',
                               description="test")
        print(ret.toJSON())
        self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)


        ret = conn.dropSchema(dbType=DBType.DBNODE,schemaName="test_schema_1")
        print(ret.toJSON())
        self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)


        ret = conn.dropSchema(dbType=DBType.DBEDGE,schemaName="test_schema_1")
        print(ret.toJSON())
        self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)

        ret = conn.dropGraph(self.gname,RequestConfig(graphName=self.gname))
        self.assertEqual(ret.status.code,ULTIPA.Code.SUCCESS)






