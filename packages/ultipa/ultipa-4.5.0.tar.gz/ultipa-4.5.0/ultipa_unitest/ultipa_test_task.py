import unittest
from ultipa import *
from ultipa import Connection,ULTIPA_REQUEST,ULTIPA
from ultipa_unitest.helper import GetTestConnection
from ultipa_unitest import conn
class TestUltipaMethods(unittest.TestCase):
    #6/2 返回数据是空
    def test_showTask(self):
        # ret = conn.showTask(ULTIPA_REQUEST.ShowTask(limit=100))
        # ret = conn.showTask(ULTIPA_REQUEST.ShowTask(id=123,limit=100))
        # ret = conn.showTask(ULTIPA_REQUEST.ShowTask(name="test",limit=100))
        # ret = conn.showTask(ULTIPA_REQUEST.ShowTask(status="pending"))
        ret = conn.showTask(ULTIPA_REQUEST.ShowTask(name="*", status="*"))
        print(ret.toJSON())

        # for i in ret.data:
        #     print("*" * 50)
        #     print(i.task_info)
        #     print(i.task_info.return_type.is_wirte_back)
        #     print(i.task_info.algo_name)
        #     print(i.param)
        #     print(i.result)
        #     print(i.toJSON())
        # print(ret.toJSON())
        # ret = conn.showTask(ULTIPA_REQUEST.ShowTask(filter={'name':'out_degree'}))
        # print(ret.toJSON())
        #
        # ret = conn.clearTask(ULTIPA_REQUEST.ClearTask(id=[1],name='out_degree'))
        # print(ret.status.code)
        #
        # ret = conn.stat(RequestConfig())
        # print(ret.toJSON())

    def test_clearTask(self):
        ret = conn.clearTask(ULTIPA_REQUEST.ClearTask(status="pending"), RequestConfig())
        print(ret.toJSON())

    # def test_pauseTask(self):
    #     ret  = conn.pauseTask(ULTIPA_REQUEST.PauseTask(all=True))
    #     print(ret.toJSON())
    #
    # def test_resumeTask(self):
    #     ret = conn.resumeTask(ULTIPA_REQUEST.ResumeTask(all=True))
    #     print(ret.toJSON())

    def test_stopTask(self):
        ret = conn.stopTask(ULTIPA_REQUEST.StopTask(all=False))
        print(ret.toJSON())


    def test_top(self):
        ret = conn.top()
        # ret = conn.stats()
        ret.Print()
        print(ret.data)
        # for i in ret.data:
        #    print(i.process_uql)
        print(ret.toJSON())

    def test_kill(self):
        conn.kill(ULTIPA_REQUEST.Kill(id='123',all=True))

