import unittest

from ultipa import ULTIPA_REQUEST, ULTIPA, ALGO_REQUEST
from ultipa_unitest import conn


class TestUltipaMethods(unittest.TestCase):

    gname = 'default'
    def test_outdegree(self):

        # ret = conn.algo_out_degree(ALGO_REQUEST.Out_Degree(node_id='12'))
        # self.assertEqual(ret.status.code,ULTIPA.Code.SUCCESS)

        ret = conn.algo_out_degree(ALGO_REQUEST.Out_Degree(node_id=12),RequestConfig(graphSetName=self.gname))
        for i in ret.data.tables:
            print(i.rows)
        print(ret.toJSON())
        # self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)
        #
        # ret = conn.algo_out_degree_all(ALGO_REQUEST.Out_Degree_All(),RequestConfig(graphSetName=self.gname))
        # self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)


    def test_indegree(self):
        ret = conn.algo_in_degree(ALGO_REQUEST.In_Degree(node_id=12),RequestConfig(graphSetName=self.gname))
        print(ret.toJSON())
        # self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)

        # ret = conn.algo_in_degree(ALGO_REQUEST.In_Degree(node_id=12, edge_property_name='rank'),RequestConfig(graphSetName=self.gname))
        # self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)

        # ret = conn.algo_in_degree_all(ALGO_REQUEST.In_Degree_All(),RequestConfig(graphSetName=self.gname))
        # self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)



    def test_degree(self):
        ret = conn.algo_degree(ALGO_REQUEST.Degree(node_id=12),RequestConfig(graphSetName=self.gname))
        self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)

        ret = conn.algo_degree(ALGO_REQUEST.Degree(node_id=12, edge_property_name='rank'),RequestConfig(graphSetName=self.gname))
        self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)

        # ret = conn.algo_degree_all(ALGO_REQUEST.Degree_All(),RequestConfig(graphSetName=self.gname))
        # self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)

    def test_algo_closeness(self):
        ret = conn.algo_closeness(ALGO_REQUEST.Closeness(ids=[12]),RequestConfig(graphSetName=self.gname))
        self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)

        ret = conn.algo_closeness(ALGO_REQUEST.Closeness(ids=[12]),RequestConfig(graphSetName=self.gname))
        self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)

        ret = conn.algo_closeness_all(ALGO_REQUEST.Closeness_All(ids=[12]),RequestConfig(graphSetName=self.gname))
        self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)

    def test_algo_in_closeness(self):
        ret = conn.algo_in_closeness(ALGO_REQUEST.In_Closeness(ids=[12]),RequestConfig(graphSetName=self.gname))
        self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)

        ret = conn.algo_in_closeness(ALGO_REQUEST.In_Closeness(ids=[12]),RequestConfig(graphSetName=self.gname))
        self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)

        ret = conn.algo_in_closeness_all(ALGO_REQUEST.In_Closeness_All(ids=[12]),RequestConfig(graphSetName=self.gname))
        self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)


    def test_algo_out_closeness(self):
        ret = conn.algo_out_closeness(ALGO_REQUEST.Out_Closeness(ids=[12]),RequestConfig(graphSetName=self.gname))
        self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)

        ret = conn.algo_out_closeness(ALGO_REQUEST.Out_Closeness(ids=[12]),RequestConfig(self.gname))
        self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)

        ret = conn.algo_out_closeness_all(ALGO_REQUEST.Out_Closeness_All(ids=[12]),RequestConfig(graphSetName=self.gname))
        self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)

    def test_algo_graph_centrality(self):
        ret = conn.algo_graph_centrality(ALGO_REQUEST.Graph_Centrality(node_id=12),RequestConfig(graphSetName=self.gname))
        self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)

        ret = conn.algo_graph_centrality(ALGO_REQUEST.Graph_Centrality(node_id=12),RequestConfig(graphSetName=self.gname))
        self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)

        # ret = conn.algo_graph_centrality_all(ALGO_REQUEST.Graph_Centrality_All(node_id=12),RequestConfig(graphSetName=self.gname))
        # self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)

    # def test_algo_betweenness_centrality(self):
    #
    #     ret = conn.algo_betweenness_centrality(ALGO_REQUEST.Betweenness_Centrality(),RequestConfig(graphSetName=self.gname))
    #     self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)


#///***********************以下两个方法不能一起测**************************///#
    def test_out_degree_all(self):
        ret = conn.algo_out_degree_all(ALGO_REQUEST.Out_Degree_All(ids=['uql find().nodes().limit(10).select(*)']),RequestConfig(graphSetName=self.gname))
        print(ret.toJSON())
        self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)
    #
    # def test_in_degree_all(self):
    #     ret = conn.algo_in_degree_all(ALGO_REQUEST.In_Degree_All(),RequestConfig(graphSetName=self.gname))
    #     print(ret.toJSON())
    #     self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)

    def test_algo_betweenness_centrality(self):
        ret = conn.algo_betweenness_centrality(ALGO_REQUEST.Betweenness_Centrality(limit=10),
                                       RequestConfig(graphSetName=self.gname))
        print(ret.toJSON())

    def test_algo_closeness_1(self):
        ret = conn.algo_closeness(ALGO_REQUEST.Closeness(ids=['1','2'],limit=10),
                                               RequestConfig(graphSetName=self.gname))
        print(ret.toJSON())


    def test_khop_all(self):
        ret = conn.algo_khop_all(ALGO_REQUEST.Khop_all(depth=3,type=1,direction='left',me='1'),
                                               RequestConfig(graphSetName=self.gname))
        print(ret.toJSON())


    # def test_khop(self):
    #     ret = conn.algo_k_hop(ALGO_REQUEST.Khop(depth=3,type=1),
    #                                            RequestConfig(graphSetName=self.gname))
    #     print(ret.toJSON())







