import random
import unittest
from ultipa import *
from ultipa import Connection, ULTIPA_REQUEST, ULTIPA
from ultipa.utils.privileges import GraphPrivileges, SystemPrivileges
from ultipa_unitest import conn
from datetime import datetime





class TestUltipaMethods(unittest.TestCase):


    #4.0
    def test_listpolicy(self):
        ret = conn.showPolicy()
        # ret = conn.getPolicy(ULTIPA_REQUEST.GetPolicy('test'))
        print(ret.toJSON())
        # for i in ret.data:
        #     for i in i.graphPrivileges:
        #         print(i.values)
        #         print(i.name)
        # print(ret.toJSON(pretty=True))
        # self.assertEqual(ret.status.code,ULTIPA.Code.SUCCESS)

    def test_listPrivilege(self):
        ret = conn.showPrivilege()
        print(ret.toJSON())
        # for i in ret.data:
        #     print(i.graphPrivileges)
        # print(ret.toJSON())
        # self.assertEqual(ret.status.code,ULTIPA.Code.SUCCESS)

    def test_createpolicy(self):
        ret = conn.createPolicy(ULTIPA_REQUEST.Policy(name='sales',graphPrivileges={"default":[GraphPrivileges.FIND]},systemPrivileges=[SystemPrivileges.CREATE_POLICY]))
        # ret = conn.createPolicy(ULTIPA_REQUEST.Policy(name='sales1', systemPrivileges=['QUERY'],
        #                                               graphPrivileges=ULTIPA_REQUEST.GraphPrivilege(data={'default':['LTE']}),policies=["sales"]))
        # self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)
        print(ret.toJSON(pretty=True))
        # self.assertEqual(ret.status.code,ULTIPA.Code.SUCCESS)
    def test_updatePolicy(self):
        ret  = conn.alterPolicy(ULTIPA_REQUEST.AlterPolicy(name='sales',graphPrivileges={"default":[GraphPrivileges.AB,GraphPrivileges.FIND]},systemPrivileges=[SystemPrivileges.CREATE_POLICY]))
        print(ret.toJSON())

    def test_dropPolicy(self):
        ret = conn.dropPolicy(ULTIPA_REQUEST.DropPolicy(name="sales"))
        print(ret.toJSON())

    def test_policy(self):
        ret = conn.showPrivilege()
        print(ret)
        self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)
        ret.Print()

        ret = conn.showPolicy()
        self.assertEqual(ret.status.code,ULTIPA.Code.SUCCESS)
        ret.Print()


        ret = conn.createPolicy(ULTIPA_REQUEST.Policy(name='sales',systemPrivileges=[SystemPrivileges.CREATE_POLICY],graphPrivileges={"default":[GraphPrivileges.FIND]}))
        print(ret.toJSON())
        self.assertEqual(ret.status.code,ULTIPA.Code.SUCCESS)

        ret = conn.getPolicy(ULTIPA_REQUEST.Policy(name='sales'))
        self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)
        ret.Print()

        # ret = conn.updatePolicy(ULTIPA_REQUEST.AlterPolicy(name='sales', systemPrivileges=['QUERY','DELETE']))  # 返回的创建成功
        # print(ret.toJSON())
        #
        # ret = conn.deletePolicy(ULTIPA_REQUEST.DropPolicy(name='sales'))
        # self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)
        # #
        # #
        # ret = conn.grantPolicy(ULTIPA_REQUEST.GrantPolicy(username='test', systemPrivileges=['QUERY']))
        # self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)
        #
        # ret = conn.revokePolicy(ULTIPA_REQUEST.RevokePolicy(username='test', systemPrivileges=['QUERY']))
        # self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)

    def test_get(self):
        ret = conn.getPolicy(ULTIPA_REQUEST.GetPolicy(name='pytest_p_70__361_90349194'))
        print(ret.toJSON())


    def test_policy_flow(self):
        ret = conn.createUser(ULTIPA_REQUEST.CreateUser(username='test_policy',password='abc123456'))
        self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)
        ret = conn.grantPolicy(ULTIPA_REQUEST.GrantPolicy())

    #4.0
    def test_grant_policy(self):
        ret = conn.createUser(ULTIPA_REQUEST.CreateUser(username="ultipa",password="123456",graphPrivileges={'default':[GraphPrivileges.LTE]},systemPrivileges=[SystemPrivileges.SHOW_GRAPH],policies=['sales']))
        print(ret.toJSON())
        ret = conn.grantPolicy(ULTIPA_REQUEST.GrantPolicy(username='ultipa',graphPrivileges={'*':['LTE']},policies=['sales']))
        print(ret.toJSON())


    def test_show_privilege(self):
        ret = conn.showPrivilege()
        print(ret.toJSON())

    #4.0
    def test_revoke_policy(self):
        ret = conn.revokePolicy(ULTIPA_REQUEST.RevokePolicy('ultipa', graphPrivileges={'*':['LTE']}))
        print(ret.toJSON())

    username_prefix: str = "pytest_u_%d_" % (random.randint(0, 1000))

    def get_random_with_prefix(self, prefix: str):
        return "%s_%d_%d" % (
            prefix, random.randint(1, 1000), int((datetime.now().timestamp() * 1000) % (10e+7)))

    def isSuccess(self, res: ULTIPA_RESPONSE.Response) -> bool:
        '''
        判断是否成功
        :param res:
        :return: response的status的code码是否与预定义的code一致
        '''

        return res.status.code == ULTIPA.Code.SUCCESS

    def assertSuccess(self, res: ULTIPA_RESPONSE.Response, success: bool):
        assert self.isSuccess(res=res) == success, res.toJSON()

    def recreate_random_user_safe(self):
        """重新创建一个用户"""
        username = self.get_random_with_prefix(self.username_prefix)
        res = conn.createUser(request=ULTIPA_REQUEST.CreateUser(
            username=username,
            password=username
        ))
        self.assertSuccess(res, True)
        return username

    def create_new_connection(self, username: str, password: str):
        host = "192.168.1.65:60061"
        username = username and username or "root"
        password = password and password or "root"
        defaultConfig = UltipaConfig()
        defaultConfig.responseWithRequestInfo = True
        defaultConfig.consistency = True
        defaultConfig.responseIsMarge = True
        defaultConfig.username=username
        defaultConfig.password=password
        return Connection(host=host,defaultConfig=defaultConfig)

    def test_test_insert(self):
        user  = self.recreate_random_user_safe()
        conn1 = self.create_new_connection(username=user, password=user)
        res = conn1.insertEdge(request=ULTIPA_REQUEST.InsertEdge([{}], schema="default"),
                              requestConfig=RequestConfig(
            graphName='default'
        ))
        print(res.toJSON())


    def test_test_insert_bulk(self):
        user  = self.recreate_random_user_safe()
        conn1 = self.create_new_connection(username=user, password=user)
        results = [{"schema": "default", "values": [{}]}]
        res = conn1.insertNodesBulk(ULTIPA_REQUEST.InsertNodeBulk(rows=results,insertType=ULTIPA.InsertType.UPSERT),
                              requestConfig=RequestConfig(
            graphName='default'
        ))
        print(res.toJSON())


    def test_export(self):
        user = self.recreate_random_user_safe()
        conn1 = self.create_new_connection(username=user, password=user)
        schemaName="default"

        ret = conn1.export(request=ULTIPA_REQUEST.Export(
            type=DBType.DBNODE,
            limit=10, schema=schemaName
        ), requestConfig=RequestConfig(graphName='default'))
        print(ret.toJSON())








