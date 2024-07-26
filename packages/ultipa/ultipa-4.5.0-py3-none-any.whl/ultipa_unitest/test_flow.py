import time
import unittest

from ultipa import ULTIPA_REQUEST, ULTIPA
from ultipa.types.types_request import CommonSchema
from ultipa.utils.privileges import GraphPrivileges, SystemPrivileges
from ultipa_unitest import conn


class TestUltipaFlowMethods(unittest.TestCase):
    gname = 'default'

    def check_graph(self, data, graph):
        ret1 = list(filter(lambda x: x.name == graph, data))
        return False if len(ret1) == 0 else True

    def test_graph_flow(self):
        graphName = "test12"
        ret = conn.showGraph()
        self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)
        self.assertEqual(self.check_graph(ret.data, graphName), False)

        ret = conn.createGraph(ULTIPA_REQUEST.Graph(graph=graphName))
        self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)
        ret = conn.showGraph()
        self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)
        self.assertEqual(self.check_graph(ret.data, graphName), True)

        newGraph = "test_new"
        ret = conn.alterGraph(ULTIPA_REQUEST.AlterGraph(graph=graphName, new_name=newGraph))
        self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)
        ret = conn.showGraph()
        self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)
        self.assertEqual(self.check_graph(ret.data, newGraph), True)

        ret = conn.dropGraph(ULTIPA_REQUEST.Graph(graph=newGraph))
        self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)
        ret = conn.showGraph()
        self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)
        self.assertEqual(self.check_graph(ret.data, newGraph), False)

    def check_schema(self, data, graph):
        ret1 = list(filter(lambda x: x.name == graph, data))
        return False if len(ret1) == 0 else True

    def test_schema_flow(self):
        schema = "test_s"
        new_schema = "test_new"
        for type in [DBType.DBNODE, DBType.DBEDGE]:
            ret = conn.showSchema()
            self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)
            ret = conn.createSchema(ULTIPA_REQUEST.CreateSchema(name=schema, type=type))
            self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)

            ret = conn.showSchema()
            self.assertEqual(self.check_schema(ret.data.nodeSchemas.schemaRows, schema), True)

            conn.alterSchema(ULTIPA_REQUEST.AlterSchema(type=type, schema=schema, new_name=new_schema))
            ret = conn.showSchema()
            self.assertEqual(self.check_schema(ret.data.nodeSchemas.schemaRows, new_schema), True)

            conn.dropSchema(ULTIPA_REQUEST.DropSchema(type=type, schema=new_schema))
            ret = conn.showSchema()
            self.assertEqual(self.check_schema(ret.data.nodeSchemas.schemaRows, new_schema), False)

    def check_property(self, data, property):
        ret1 = list(filter(lambda x: x.propertyName == property, data))
        return False if len(ret1) == 0 else True

    def test_property_flow(self):
        schema = "test_property"
        property = "test_p"
        for type in [DBType.DBNODE, DBType.DBEDGE]:
            ret = conn.createSchema(ULTIPA_REQUEST.CreateSchema(name=schema, type=type))
            self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)
            ret = conn.createProperty(
                ULTIPA_REQUEST.CreateProperty(type, ULTIPA_REQUEST.CommonSchema(schema=schema, property=property)))
            self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)
            ret = conn.getProperty(ULTIPA_REQUEST.GetProperty(type=type, schema=schema))
            self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)
            self.assertEqual(self.check_property(ret.data, property), True)
            ret = conn.dropSchema(ULTIPA_REQUEST.DropSchema(type=type, schema=schema))
            self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)

    def check_user(self, data, user):
        ret1 = list(filter(lambda x: x.username == user, data))
        return False if len(ret1) == 0 else True

    def test_user_flow(self):
        new_user_name = "test_user"
        ret = conn.showUser()
        self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)
        conn.createUser(ULTIPA_REQUEST.CreateUser(username=new_user_name, password=new_user_name))
        ret = conn.showUser()
        self.assertEqual(self.check_user(ret.data, new_user_name), True)
        self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)
        ret = conn.dropUser(ULTIPA_REQUEST.DropUser(username=new_user_name))
        self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)

    def check_policy(self,data, policy):
        ret1 = list(filter(lambda x: x.name == policy, data))
        return False if len(ret1) == 0 else True

    def test_policy_flow(self):
        new_policy = "test_policy"
        ret = conn.showPolicy()
        self.assertEqual(self.check_policy(ret.data, new_policy), False)
        ret = conn.createPolicy(ULTIPA_REQUEST.CreatePolicy(name=new_policy,graphPrivileges={'default':[GraphPrivileges.LTE]},systemPrivileges=[SystemPrivileges.SHOW_GRAPH]))
        self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)
        ret = conn.showPolicy()
        self.assertEqual(self.check_policy(ret.data, new_policy), True)
        ret = conn.dropPolicy(ULTIPA_REQUEST.DropPolicy(name=new_policy))
        self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)
        ret = conn.showPrivilege()
        print(ret.toJSON())







