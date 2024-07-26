import unittest

from helper import GetTestConnection
from ultipa import *
from ultipa import Connection,ULTIPA_REQUEST,ULTIPA
from ultipa_unitest import conn


class TestUltipaMethods(unittest.TestCase):
    #4.0
    def test_create_user(self):
        ret = conn.createUser(ULTIPA_REQUEST.CreateUser(username='ultipa',password='ultipa',graphPrivileges={"default": ['UFE']},systemPrivileges=["STAT","TOP"]))
        print(ret.toJSON())
        # self.assertEqual(ret.status.code,ULTIPA.Code.SUCCESS)

    #4.0
    def test_list_user(self):
        ret = conn.showUser(RequestConfig())
        print(ret.toJSON())
        ret.Print()


    #4.0
    #TODO BUG no password
    def test_update_user(self):
        ret = conn.alterUser(ULTIPA_REQUEST.AlterUser(username='ultipa',graph_privileges={"*": ['UFE']}))
        print(ret.toJSON())
        # self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)

    #4.0
    def test_get_user(self):
        # ret = conn.showUser()
        ret = conn.getUser(username="root")
        print(ret.toJSON())

        print(ret.data.username)
        print(ret.data.create)
        # print(ret.data.username)
        # for i in ret.data.graph_privileges:
        #     print('>>>',i.values)
        #     print('*.',i.name)

        # print(type(ret.data))
        # print(ret.toJSON())
        # u = ret.data
        # print('--------------------------')
        # print(u.__dict__)
        # print(u.username, u.system_privileges)
    def test_delete_user(self):
        ret = conn.dropUser(ULTIPA_REQUEST.DropUser(username='ultipa'))
        print(ret.toJSON())

    def test_getSelfInfo(self):
        ret = conn.getSelfInfo()

        print(ret.toJSON())


    def test_flow(self):
        host = "210.13.32.146:60075"
        username="ultipa1111"
        ret = conn.createUser(
            ULTIPA_REQUEST.CreateUser(username=username, password=username, graph_privileges={"default": ['CREATE']},
                                      system_privileges=["POLICY"]))
        print(ret.toJSON())
        defaultConfig = UltipaConfig()
        defaultConfig.responseWithRequestInfo = True
        defaultConfig.consistency = False
        defaultConfig.responseIsMarge = True
        conn1 = Connection(host=host, username=username, password=username,
                          defaultConfig=defaultConfig)
        # conn1 = GetTestConnection(host="210.13.32.146:60075", username=username, password=username)
        ret1= conn1.uql("create().graph(\"test\")")
        print(ret1.toJSON())






