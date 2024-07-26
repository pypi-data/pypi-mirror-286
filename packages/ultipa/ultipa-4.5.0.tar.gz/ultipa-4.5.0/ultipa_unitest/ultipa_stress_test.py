import random
import unittest

from ultipa import ULTIPA_REQUEST, ULTIPA
from ultipa_unitest import conn


class TestUltipaMethods(unittest.TestCase):



    def random_autoNet(self,):
        node_ret = self.ret.data.get('totalNodes')
        srcs = [self.random_node(node_ret) for i in range(random.randint(1,10))]
        # ret = conn.autoNet(ULTIPA_REQUEST.AutoNet(srcs=srcs,depth=3,limit=2))
        # self.assertEqual(ret.status.code,ULTIPA.Code.SUCCESS)
        dets = [self.random_node(node_ret) for i in range(random.randint(1,10))]
        ret = conn.autoNet(ULTIPA_REQUEST.AutoNet(srcs=srcs,dests=dets,depth=3,limit=2,select=['name']))
        # self.assertEqual(ret.status.code,ULTIPA.Code.SUCCESS)
        return ret.toJSON()




    def random_searchAB(self):
        node_ret = self.ret.data.get('totalNodes')
        src = self.random_node(node_ret)
        dest = self.random_node(node_ret)
        depth = random.randint(1,5)
        ret = conn.searchAB(
            ULTIPA_REQUEST.SearchAB(src, dest, depth, 10,select=['*']))
        self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)
        return ret.toJSON()


    def random_searchKhop(self):
        node_ret = self.ret.data.get('totalNodes')
        src = self.random_node(node_ret)
        depth = random.randint(1, 5)
        ret = conn.searchKhop(
            ULTIPA_REQUEST.Searchkhop(src, depth, 10, select=['*']))
        self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)
        return ret.toJSON()

    def random_nodeSpread(self):
        node_ret = self.ret.data.get('totalNodes')
        src = self.random_node(node_ret)
        depth = random.randint(1, 5)
        ret = conn.nodeSpread(
            ULTIPA_REQUEST.NodeSpread(src, depth, 10, select=['*']))
        self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)
        return ret.toJSON()


    def test_main(self):
        self.ret = conn.stat()
        from multiprocessing.dummy import Pool as MPThreadPool
        tpool = MPThreadPool(100)
        results=[]
        for i in range(1000):
            print(i)
            # result = tpool.apply_async(self.random_autoNet)
            # result = tpool.apply_async(self.random_searchAB)
            # result = tpool.apply_async(self.random_searchKhop)
            result = tpool.apply_async(self.random_nodeSpread)
            results.append(result)
        for result in results:
            result.wait()
            print(result.get())

        print('over')



    def random_node(self,noderet):
        nodeid = str(random.randint(1,int(noderet)))
        return nodeid
