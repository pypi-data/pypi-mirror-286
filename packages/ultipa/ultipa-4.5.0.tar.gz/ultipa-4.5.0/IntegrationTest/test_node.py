import unittest
from ultipa import *
from ultipa import Connection, ULTIPA_REQUEST, ULTIPA, FILTER
from ultipa_unitest import conn


class TestUltipaMethods(unittest.TestCase):
    gname = 'default'

    def test_insert(self):
        #create_node_case_1
        ret = conn.insertNode(ULTIPA_REQUEST.InsertNode([{"name": "pytest"}]), RequestConfig())
        self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)

        headers = [{"name": "name", "type": "PROPERTY_STRING"}]
        row = [{"name": "pytest"}]
        ret = conn.insertNodesBulk(ULTIPA_REQUEST.InsertNodeBulk(headers=headers, rows=row), RequestConfig())
        self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)

        #create_node_case_2

        ret = conn.insertNode(ULTIPA_REQUEST.InsertNode([{}]), RequestConfig())
        self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)

        headers = [{"name": "name", "type": "PROPERTY_STRING"}]
        row = [{}]
        ret = conn.insertNodesBulk(ULTIPA_REQUEST.InsertNodeBulk(headers=headers, rows=row), RequestConfig())
        self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)


        headers = [{"name": "name", "type": "PROPERTY_STRING"}]
        row = [{"name": "pytest"}]
        ret = conn.insertNodesBulk(ULTIPA_REQUEST.InsertNodeBulk(headers=headers, rows=row, silent=True),
                                   RequestConfig())
        self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)

        headers = [{"name": "name", "type": "PROPERTY_STRING"}]

        ret = conn.getGraph(ULTIPA_REQUEST.GraphInfo(graphSetName=self.gname),RequestConfig())
        ret = ret.toDict()
        id = ret.get('data').get('totalNodes')
        row = [{'_id': str(int(id)+1), "name": "pytest"}]
        ret = conn.insertNodesBulk(ULTIPA_REQUEST.InsertNodeBulk(headers=headers, rows=row, customId=True),
                                   RequestConfig())
        self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)

        ret = conn.insertNode(ULTIPA_REQUEST.InsertNode([{"name": "pytest"},{"name": "pytest1"}]), RequestConfig())
        self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)








