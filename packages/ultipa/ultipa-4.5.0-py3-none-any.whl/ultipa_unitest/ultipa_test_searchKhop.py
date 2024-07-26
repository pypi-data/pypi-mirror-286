import unittest
from ultipa import *
from ultipa import Connection, ULTIPA_REQUEST, ULTIPA
from ultipa_unitest import conn
from typing import List


class TestUltipaMethods(unittest.TestCase):

    gname = 'default'

    def test_searchKhop1(self):
        filt = FILTER.LtFilter(name='age',value=28)
        ret = conn.searchKhop(ULTIPA_REQUEST.Searchkhop(12,node_filter=filt.builder(),depth=3,limit=30,select=['name']),RequestConfig(graphSetName=self.gname))
        print(ret.toJSON())
        # for i in  ret.data.nodes:
        #     print(i.id)
        #     print(i.values)
        #
        # print(ret.toJSON())

    def test_searchKhop(self):
        ret = conn.searchKhop(ULTIPA_REQUEST.Searchkhop(12,depth=3,limit=5,select=['*']),RequestConfig(graphSetName=self.gname))
        print(ret.toDict())
        self.assertEqual(ret.status.code,ULTIPA.Code.SUCCESS)
        ret = conn.searchKhop(ULTIPA_REQUEST.Searchkhop(12, depth=3, limit=5, select=['name']),RequestConfig(graphSetName=self.gname))
        self.assertEqual(ret.status.code,ULTIPA.Code.SUCCESS)

        noFilter = ULTIPA_REQUEST.FILTER.EqFilter('age',31)
        ret = conn.searchKhop(ULTIPA_REQUEST.Searchkhop(12, depth=1, limit=10, node_filter=noFilter.builder(), select=['name', 'age']),RequestConfig(graphSetName=self.gname))
        print(ret.toJSON())
        self.check_node_age(ret,'eq',31,name='age')

        noFilter = ULTIPA_REQUEST.FILTER.BtFilter('age',[13,20])
        ret = conn.searchKhop(ULTIPA_REQUEST.Searchkhop(12, depth=1, limit=10, node_filter=noFilter.builder(), select=['age']),RequestConfig(graphSetName=self.gname))
        self.check_node_age(ret, 'bt',13,20,name='age')

        noFilter = ULTIPA_REQUEST.FILTER.LtFilter('age', 13)
        print(noFilter.builder())
        ret = conn.searchKhop(ULTIPA_REQUEST.Searchkhop(12, depth=1, limit=10, node_filter=noFilter.builder(), select=['age']),RequestConfig(graphSetName=self.gname))
        print(ret.toJSON())
        self.check_node_age(ret, 'lt', 13,name='age')

        noFilter = ULTIPA_REQUEST.FILTER.LteFilter('age', 13)
        ret = conn.searchKhop(ULTIPA_REQUEST.Searchkhop(12, depth=1, limit=10, node_filter=noFilter.builder(), select=['age']),RequestConfig(graphSetName=self.gname))
        self.check_node_age(ret, 'lte', 13,name='age')

        noFilter = ULTIPA_REQUEST.FILTER.GtFilter('age', 13)
        ret = conn.searchKhop(ULTIPA_REQUEST.Searchkhop(12, depth=1, limit=10, node_filter=noFilter.builder(), select=['age']),RequestConfig(graphSetName=self.gname))
        self.check_node_age(ret, 'gt', 13,name='age')

        noFilter = ULTIPA_REQUEST.FILTER.GteFilter('age', 13)
        ret = conn.searchKhop(ULTIPA_REQUEST.Searchkhop(12, depth=1, limit=10, node_filter=noFilter.builder(), select=['age']),RequestConfig(graphSetName=self.gname))
        self.check_node_age(ret, 'gte', 13,name='age')

        noFilter = ULTIPA_REQUEST.FILTER.InFilter('age', [18, 20, 22, 80])
        ret = conn.searchKhop(ULTIPA_REQUEST.Searchkhop(12, depth=1, limit=10, node_filter=noFilter.builder(), select=['age']),RequestConfig(graphSetName=self.gname))
        self.check_node_age(ret, 'in',values=[18, 20, 22, 80],name='age')

        noFilter = ULTIPA_REQUEST.FILTER.OrFilter([ULTIPA_REQUEST.FILTER.EqFilter('age',20),ULTIPA_REQUEST.FILTER.EqFilter('name', 'Hubert Pirtle')])
        print(noFilter.builder())
        ret = conn.searchKhop(ULTIPA_REQUEST.Searchkhop(12,depth=1, limit=10,
                                      node_filter=noFilter.builder(),
                                      select=['name', 'age']),RequestConfig(graphSetName=self.gname))
        print(ret.toJSON())
        self.assertEqual(ret.status.code,ULTIPA.Code.SUCCESS)

        # noFilter = ULTIPA_REQUEST.FILTER.EqFilter('age', 31)
        # ret = conn.searchKhop(ULTIPA_REQUEST.Searchkhop(12, depth=1, limit=10, node_filter={'age': {'$and': [{'age': 40}, {'name': "Chad Biles"}]}},
        #                               select=['name', 'age']),RequestConfig(graphSetName=self.gname))
        #
        # self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)

        noFilter = ULTIPA_REQUEST.FILTER.GteFilter('age', 13)
        ret = conn.searchKhop(ULTIPA_REQUEST.Searchkhop(12, depth=1, limit=10, node_filter=noFilter.builder(), select=['age']),RequestConfig(graphSetName=self.gname))
        self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)

    def check_node_age(self,ret, rtype:str, smallValue:int=None, bigValue:int=None,values:List[int]=None,name:str=''):
        if values is None:
            values=[]
        for va in ret.toDict().get('data').get('nodes'):
            va = va.get('values')
            age = int(va.get(name))
            if rtype == 'lt':
                self.assertIsNone(self.assertLess(age, smallValue))
            elif rtype == 'lte':
                self.assertIsNone(self.assertLessEqual(age, smallValue))
            elif rtype == 'gt':
                self.assertIsNone(self.assertGreater(age, smallValue))
            elif rtype == 'gte':
                self.assertIsNone(self.assertGreaterEqual(age, smallValue))
            elif rtype == 'bt':
                self.assertIsNone(
                    self.assertGreaterEqual(age, smallValue) and self.assertLessEqual(age,bigValue))

            elif rtype== 'in':
                self.assertIn(age,values)