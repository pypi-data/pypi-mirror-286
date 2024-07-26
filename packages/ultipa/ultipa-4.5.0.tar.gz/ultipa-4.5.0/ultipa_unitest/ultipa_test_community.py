import unittest

from ultipa import ULTIPA_REQUEST, ULTIPA, ALGO_REQUEST
from ultipa_unitest import conn


class TestUltipaMethods(unittest.TestCase):
    gname = 'default'

    def test_algo_k_hop(self):
        ret = conn.algo_khop_all(ALGO_REQUEST.khop_all(depth=3), RequestConfig(graphSetName=self.gname))
        self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)

    def test_algo_knn(self):
        ret = conn.algo_knn(ALGO_REQUEST.knn(node_id=2, node_property_names=['name'], top_k=10, target_property_name='name'),
                            RequestConfig(graphSetName=self.gname))
        self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)

    def test_algo_k_core(self):
        ret = conn.algo_k_core(ALGO_REQUEST.k_core(k=1), RequestConfig(graphSetName=self.gname))
        self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)

    def test_algo_mst(self):
        ret = conn.algo_mst(ALGO_REQUEST.mst(ids=[12,21], edge_property_name='rank'),
                            RequestConfig(graphSetName=self.gname))
        print(ret.toJSON())
        self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)
        # ret = conn.algo_mst(ALGO_REQUEST.Mst(ids=[12,21], edge_property_name='rank'),
        #                     RequestConfig(graphSetName=self.gname))
        # self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)

    def test_algo_page_rank(self):
        ret = conn.algo_page_rank(ALGO_REQUEST.page_rank(loop_num=1, damping=0.1),
                                  RequestConfig(graphSetName=self.gname))
        self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)

    def test_algo_sybil_rank(self):
        ret = conn.algo_sybil_rank(
            ALGO_REQUEST.sybil_rank(loop_num=1, sybil_num=1, trust_seeds=[1, 2, 3, 4, 5], total_trust=2),
            RequestConfig(graphSetName=self.gname))
        self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)

    def test_jaccard(self):
        ret = conn.algo_jaccard(ALGO_REQUEST.jaccard(ids1=[1884,], ids2=[4801,]),
                                RequestConfig(graphSetName=self.gname))
        print(ret.toJSON())
        self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)

        # ret = conn.algo_jaccard(ALGO_REQUEST.Jaccard('12',top=5))
        # self.assertEqual(ret.status.code,ULTIPA.Code.SUCCESS)
        #
        # ret = conn.algo_jaccard(ALGO_REQUEST.Jaccard('12','21',top=5))
        # self.assertEqual(ret.status.code,ULTIPA.Code.SUCCESS)

    def test_algo_cosine_similarity(self):
        ret = conn.algo_cosine_similarity(
            ALGO_REQUEST.cosine_similarity(node_id1=12, node_id2=21, node_property_names=['name', 'age']),
            RequestConfig(graphSetName=self.gname))
        self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)

    def test_algo_connected_component(self):
        ret = conn.algo_connected_component(ALGO_REQUEST.connected_component(cc_type=1,write_back=True),
                                            RequestConfig(graphSetName=self.gname))
        print(ret.toJSON())
        self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)

    def test_algo_lpa(self):
        ret = conn.algo_lpa(ALGO_REQUEST.lpa(loop_num=2, node_property_name='name'),
                            RequestConfig(graphSetName=self.gname))
        print(ret.toJSON())
        self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)

    def test_algo_hanp(self):
        ret = conn.algo_hanp(
            ALGO_REQUEST.hanp(loop_num=2, edge_property_name='rank', node_property_name='name', m=0.1, delta=0.1),
            RequestConfig(graphSetName=self.gname))
        print(ret.toJSON())
        self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)

    def test_algo_k_means(self):
        ret = conn.algo_k_means(
            ALGO_REQUEST.k_means(start_ids=[12,21,79],k=1,node_property_names=['name','age'],distance_type=1,loop_num=1),
            RequestConfig(graphSetName=self.gname))
        print(ret.toJSON())
        self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)

    def test_algo_louvain(self):
        ret = conn.algo_louvain(
            ALGO_REQUEST.louvain(phase1_loop_num=1, min_modularity_increase=1),
            RequestConfig(graphSetName=self.gname))
        print(ret.toJSON())
        self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)

    def test_algo_triangle_counting(self):
        ret = conn.algo_triangle_counting(ALGO_REQUEST.triangle_counting(),
                                          RequestConfig(graphSetName=self.gname))
        print(ret.toJSON())
        self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)

    def test_algo_hyperANF(self):
        ret = conn.algo_hyperANF(ALGO_REQUEST.hyperANF(loop_num=1,register_num=1),
                                          RequestConfig(graphSetName=self.gname))
        print(ret.toJSON())
        self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)

    def test_algo_common_neighbours(self):
        ret = conn.algo_common_neighbours(ALGO_REQUEST.common_neighbours(node_id1=12,node_id2=21),
                                          RequestConfig(graphSetName=self.gname))
        self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)

    def test_algo_subgraph(self):
        ret = conn.algo_subgraph(ALGO_REQUEST.subgraph(node_ids=[12,21,123]),
                                          RequestConfig(graphSetName=self.gname))
        print(ret.toJSON())
        self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)

    def test_algo_clustering_coefficient(self):
        ret = conn.algo_clustering_coefficient(ALGO_REQUEST.clustering_coefficient(node_id='12'),
                                               RequestConfig(graphSetName=self.gname))
        print(ret.toJSON())
        self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)
