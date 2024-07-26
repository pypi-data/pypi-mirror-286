import unittest

from ultipa import ULTIPA, ALGO_REQUEST, ULTIPA_REQUEST
from ultipa_unitest import conn


class TestUltipaMethods(unittest.TestCase):
    gname = 'default'

    def test_line(self):
        ret = conn.algo_line(
            ALGO_REQUEST.Line(edge_property_name='rank', resolution=1, dimension=1, start_alpha=1, neg_num=1,
                              total_sample=1, train_order=1),RequestConfig())
        print(ret.toJSON())
        self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)

    def test_algo_random_walk(self):
        ret = conn.algo_random_walk(ALGO_REQUEST.Random_Walk(walk_num=1, walk_length=1, edge_property_name='rank'),
                                    RequestConfig(graphSetName=self.gname))
        self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)

    def test_algo_random_walk_node2vec(self):
        ret = conn.algo_random_walk_node2vec(
            ALGO_REQUEST.Random_Walk_Node2vec(walk_num=1, walk_length=1, p=1, q=1, edge_property_name='rank'),
            RequestConfig(graphSetName=self.gname))
        self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)

    def test_algo_node2vec(self):
        ret = conn.algo_node2vec(
            ALGO_REQUEST.Node2vec(walk_num=1, walk_length=1, p=1, q=1, window_size=1, dimension=1, learning_rate=1,
                                  min_learning_rate=1, resolution=1, iter_num=1, sub_sample_alpha=1, neg_num=1,
                                  min_frequency=1, edge_property_name='rank'),
            RequestConfig(graphSetName=self.gname))
        self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)

    def test_algo_random_walk_struc2vec(self):
        ret = conn.algo_random_walk_struc2vec(
            ALGO_REQUEST.Random_Walk_Stuc2vec(walk_num=1, walk_length=1, k=0.1, stay_probability=0.1),
            RequestConfig(graphSetName=self.gname))
        self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)

    def test_algo_random_struc2vec(self):
        ret = conn.algo_struc2Vec(
            ALGO_REQUEST.Struc2Vec(walk_num=1, walk_length=1, k=1, stay_probability=0.1, window_size=1, dimension=1,
                                   learning_rate=1, min_learning_rate=0.1, resolution=1, loop_num=1,
                                   sub_sample_alpha=0.1, neg_num=1, min_frequency=1),
            RequestConfig(graphSetName=self.gname))
        self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)
