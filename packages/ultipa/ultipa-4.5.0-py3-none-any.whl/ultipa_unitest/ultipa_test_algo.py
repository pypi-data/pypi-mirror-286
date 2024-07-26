import unittest
from ultipa import *
from ultipa import Connection,ULTIPA_REQUEST,ULTIPA
from ultipa_unitest import conn
import random

class TestUltipaMethods(unittest.TestCase):
    gname = 'default'

    def test_InstallAlgo(self):
        ret = conn.installAlgo(ULTIPA_REQUEST.InstallAlgo(configPath="/Users/ultipa/work/算法配置文件/mst.yml",
                                                          soPath="/Users/ultipa/work/4.1.50 算法包/libplugin_mst.so"))
        print(ret.toJSON())
        ret.Print()

    def test_UnstallAlgo(self):
        ret = conn.uninstallAlgo(ULTIPA_REQUEST.UninstallAlgo("mst"))
        print(ret.toJSON())
        ret.Print()


    def test_listAlgo(self):
        ret = conn.showAlgo(RequestConfig())
        # for algo in ret.data:
        #     print(algo.name)
        #     print(algo.param)
        #     print(algo.result_opt)
        print(ret.toJSON())

    def test_install_algo(self):
        ret = conn.installAlgo(ULTIPA_REQUEST.InstallAlgo(configPath='/Users/ultipa/work/ultipa-python-sdk2/algo/khop_all.yml',soPath="/Users/ultipa/work/ultipa-python-sdk2/algo/libplugin_khop_all.so"))
        print(ret.toJSON())

    def test_uninstall_algo(self):
        ret = conn.uninstallAlgo(ULTIPA_REQUEST.UninstallAlgo(algoName='khop_all'))
        print(ret.toJSON())


#     def test_betweenness_centrality(self):
#         ret = conn.algo_betweenness_centrality(ALGO_REQUEST.betweenness_centrality(limit=6,sample_size=-2,force=True))
#         print(ret.toJSON())
#
#
#     def test_connected_component(self):
#         ret = conn.algo_connected_component(ALGO_REQUEST.connected_component(cc_type=1))
#         print(ret.toJSON())
#
#
#     def test_clustering_coefficient_all(self):
#         ret = conn.algo_clustering_coefficient(ALGO_REQUEST.clustering_coefficient())
#         print(ret.toJSON())
#
#
#     def test_closeness(self):
#         ret = conn.algo_closeness_centrality(ALGO_REQUEST.closeness_centrality(ids=['uql find().nodes().limit(10)']))
#         print(ret.toJSON())
#
#     #不支持
#     # def test_closeness_all(self):
#     #     ret = conn.algo_closeness_all(ALGO_REQUEST.Closeness_All(ids=['uql find().nodes().limit(10)']))
#     #     print(ret.toJSON())
#
#
#
#     def test_common_neighbours(self):
#         ret = conn.algo_common_neighbours(ALGO_REQUEST.common_neighbours(ids=12,ids2=21))
#         print(ret.toJSON())
#
#
#     def test_cosine_similarity(self):
#         ret = conn.algo_cosine_similarity(ALGO_REQUEST.cosine_similarity(ids=12,ids2=21,node_schema_name="default",node_property_names=['name','age']))
#         print(ret.toJSON())
#
#     # def test_cosine_similarity_e(self):
#
#     def test_degree(self):
#         ret = conn.algo_degree(
#             ALGO_REQUEST.degree(ids=[12]))
#         print(ret.toJSON())
#
#     def test_degree_all(self):
#         ret = conn.algo_degree_all(
#             ALGO_REQUEST.degree(ids=['uql find().nodes().limit(10)']))
#         print(ret.toJSON())
#
#
#
#     # def test_out_degree(self):
#     #     ret = conn.algo_out_degree(ALGO_REQUEST.Out_Degree(node_id=12))
#     #     print(ret.toJSON())
#
#     # def test_out_degree_all(self):
#     #     ret = conn.algo_out_degree_all(ALGO_REQUEST.Out_Degree_All(ids=['uql find().nodes().limit(10)']))
#     #     print(ret.toJSON())
#     #
#     #
#     #
#     # def test_in_degree(self):
#     #     ret = conn.algo_in_degree(ALGO_REQUEST.In_Degree(node_id=12))
#     #     print(ret.toJSON())
#     #
#     # def test_in_degree_all(self):
#     #     ret = conn.algo_in_degree_all(ALGO_REQUEST.In_Degree_All(ids=['uql find().nodes().limit(10)']))
#     #     print(ret.toJSON())
#
#
#     def test_graph_centrality(self):
#         ret = conn.algo_graph_centrality(ALGO_REQUEST.graph_centrality(node_id='12'))
#         print(ret.toJSON())
#
#
#     def test_jaccard(self):
#         conn.defaultConfig.defaultGraph='amz'
#         ret = conn.algo_jaccard(ALGO_REQUEST.jaccard(ids=[1,2]))
#         print(ret.toJSON())
#
#     def test_lpa(self):
#         ret = conn.algo_lpa(ALGO_REQUEST.lpa(loop_num=3))
#         print(ret.toJSON())
#
#
#     def test_page_rank(self):
#         ret = conn.algo_page_rank(ALGO_REQUEST.page_rank(loop_num=2,write_back=True,damping=0.2))
#         print(ret.toJSON())
#
#
#     def test_triangle_counting(self):
#         ret = conn.algo_triangle_counting(ALGO_REQUEST.triangle_counting())
#         print(ret.toJSON())
#
#         ret = conn.algo_triangle_counting(ALGO_REQUEST.triangle_counting(type=2))
#         print(ret.toJSON())
#
#
#     def test_khop_all(self):
#         ret = conn.algo_khop_all(ALGO_REQUEST.khop_all(depth=3, type=1, direction='left', me='1'),
#                                  RequestConfig(graphSetName=self.gname))
#         print(ret.toJSON())
#
#
#     def test_k_core(self):
#         ret = conn.algo_k_core(ALGO_REQUEST.k_core(k=1))
#         print(ret.toJSON())
#
#     def test_k_means(self):
#         ret = conn.algo_k_means(ALGO_REQUEST.k_means(k=2,start_ids=[12,21],node_property_names=['name'],distance_type=1,loop_num=2))
#         print(ret.toJSON())
#
#     def test_algo_hyperANF(self):
#         ret = conn.algo_hyperANF(ALGO_REQUEST.hyperANF(loop_num=3,register_num=2))
#
#     def test_subgraph(self):
#         ret = conn.algo_subgraph(ALGO_REQUEST.subgraph(ids=[1,2,3]),RequestConfig(graphSetName='multi_schema_test'))
#         print(ret.toJSON())
#
#
#     def test_clustering_coefficient(self):
#         ret = conn.algo_clustering_coefficient(ALGO_REQUEST.clustering_coefficient())
#
#
#
# #   4.0 ALGO
#     def test_algo(self):
#         uql = '''algo(khop_all).params({uuids:"uql find().nodes() as nodes return nodes", k1:2, k:4}).write({file: {filename: "amz_ids"}})'''
#         ret = conn.uql(uql, requestConfig=RequestConfig(useMaster=True,graphName="amz"))
#         print(ret.toJSON())
#




