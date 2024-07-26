import csv
import datetime
import time
import unittest
from datetime import date

from ultipa import *
from ultipa import Connection, ULTIPA_REQUEST, ULTIPA, FILTER
from ultipa.connection.connection_base import ClientType
from ultipa.utils.ufilter.new_ufilter import FilterEnum
from ultipa_unitest import conn


def read_csv():
    node_list = []
    filename = '/Users/changtao/work/data/ultipa_user.csv'
    with open(filename, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)  # 提前预览列名，当下面代码写入数据时，会将其一一对应。
        for row in reader:
            userdict = dict(row)
            userdict.pop('_o')
            node_list.append(userdict)

    return node_list

class TestUltipaMethods(unittest.TestCase):
    gname = 'default'

    def test(self):
        ret = conn.test()
        print(ret)



    #4.0
    def test_search(self):
        # conn.test()
        # ret = conn.searchNode(ULTIPA_REQUEST.SearchNode(select=[ULTIPA_REQUEST.UltipaReturn(ULTIPA_REQUEST.Schema('test'),'test'),ULTIPA_REQUEST.UltipaReturn(ULTIPA_REQUEST.Schema('test'),'test',ULTIPA_REQUEST.UltipaEquation.sum,'eeee')],limit=10),RequestConfig())
        # ret = conn.searchNode(ULTIPA_REQUEST.SearchNode(select=[ULTIPA_REQUEST.UltipaReturn('test','test',ULTIPA_REQUEST.UltipaEquation.count,['eeee']),ULTIPA_REQUEST.UltipaReturn('test','test',ULTIPA_REQUEST.UltipaEquation.sum,['eeee'])],limit=10),RequestConfig())
        conn.defaultConfig.defaultGraph='douban'
        # ret = conn.searchNode(ULTIPA_REQUEST.SearchNode(select=ULTIPA_REQUEST.Return(aliasName="nodes",all=True,limit=100)))
        # print(ret.toJSON())
        # print(ret.data[0].asNodes()[0].schema)

        ret = conn.searchNode(
            ULTIPA_REQUEST.SearchNode(select=ULTIPA_REQUEST.Return(aliasName="ed", all=True, limit=100),filter=ULTIPA_REQUEST.UltipaFilter(propertyName='_uuid',filterType=FilterEnum.IN,value=[1,2,3,4])))
        print(ret.toJSON())

        # print(ret.data[0].asNodes()[0].schema)



    def test_insert_bulk_check_o(self):
        results = [{"schema":"user","values":read_csv()}]

        ret = conn.insertNodesBulk(ULTIPA_REQUEST.InsertNodeBulk(rows=results,check_o=True),
                                   RequestConfig(graphSetName="ultipa_www"))
        print(ret.toJSON())








