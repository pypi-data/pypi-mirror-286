from ultipa import Connection, ULTIPA_REQUEST, UltipaConfig, FILTER,ULTIPA

# default = DefaultConfig(graphSetName='a')
# conn = Connection(host='124.193.211.21:60062', username="root", password="root")
# conn = Connection.GetConnection(hosts=['124.193.211.21:60162','124.193.211.21:60161','124.193.211.21:60163'], username="root", password="root",defaultConfig=default)
conn = Connection.GetConnection(hosts=['124.193.211.21:60071'])
# conn = Connection(host='192.168.3.171:60061', username="root", password="root")
# ret = conn.test()
# ret = conn.searchNode(ULTIPA_REQUEST.SearchNode(limit=10))
# print(ret.toJSON())
# 如果 ret 为True表示成功连接Ultipa Server
# print(ret)
# conn.defaultConfig.defaultGraph='a'
# ret = conn.searchNode(ULTIPA_REQUEST.SearchNode(limit=10),RequestConfig(graphSetName='a'))
# print(ret.toJSON())

# ret = conn.searchEdge(ULTIPA_REQUEST.SearchEdge(limit=10))
# print(ret.toJSON())

# ret = conn.uql("find().nodes().limit(10).select(*)")
#
# print(ret.toJSON())
#
# ret = conn.uql("find().edges().limit(10).select(*)")
#
# print(ret.toJSON())
#
# ret =  conn.searchAB(ULTIPA_REQUEST.SearchAB(src=12,dest=21,depth=3,limit=5))
# print(ret.toJSON())

# ret =  conn.searchKhop(ULTIPA_REQUEST.Searchkhop(src=12,depth=1,limit=10))
# print(ret.toJSON())
# for i in ret.data.paths:
#     print(i.toJSON())
# print(ret.toJSON())

# ret = conn.nodeSpread(ULTIPA_REQUEST.NodeSpread(src=12,limit=5))
# print(ret.toJSON())

#
# ret = conn.autoNet(ULTIPA_REQUEST.AutoNet(srcs=[12,21,30,40],depth=3, limit=2,select=['name','age']))
# print(ret.toJSON())

# item1 = ULTIPA_REQUEST.TemplateNodeItem(name=ULTIPA_REQUEST.TNodeItem.n, alias='n1')
# item2 = ULTIPA_REQUEST.TemplateEdgeItem(name=ULTIPA_REQUEST.TEdgeItem.e, alias='e')
# item3 = ULTIPA_REQUEST.TemplateNodeItem(name=ULTIPA_REQUEST.TNodeItem.n, alias='n2')
# req = ULTIPA_REQUEST.Template(alias='p', items=[item1, item2, item3], limit=5, _return=['p', 'n1', 'e', 'n2'])
# ret = conn.template(request=req)
# print(ret.data.toJSON())

# ret = conn.insertNode(ULTIPA_REQUEST.InsertNode(nodes = [{'age':'20'}]))
# print(ret.toJSON())

# ret = conn.insertEdge(ULTIPA_REQUEST.InsertEdge(edges = [{'_from_id':1,'_to_id':2,'name':'help',"rank":12}]))
# print(ret.toJSON())

# filter = FILTER.EqFilter(name='id',value=2)
# ret = conn.updateNode(ULTIPA_REQUEST.UpdateNode(values={'age': 1},filter=filter))
# print(ret.toJSON())

# filter = FILTER.EqFilter(name='id',value=1)
# ret = conn.updateNode(ULTIPA_REQUEST.UpdateNode(filter=filter, values={'age': 20}))
# print(ret.toJSON())

# ret = conn.updateEdge(ULTIPA_REQUEST.UpdateEdge(filter=[1], values={'rank': 1}))
# print(ret.toJSON())

# filter = FILTER.EqFilter(name='id', value=1)
# ret = conn.updateEdge(ULTIPA_REQUEST.UpdateEdge(filter=filter, values={'rank': 20}))
# print(ret.toJSON())

# ret = conn.deleteNode(ULTIPA_REQUEST.DeleteNode(id=3))
# print(ret.toJSON())

# filter = FILTER.EqFilter(name='age', value=20)
# ret = conn.deleteNode(ULTIPA_REQUEST.DeleteNode(filter=filter))
# print(ret.toJSON())
#
# ret = conn.deleteEdge(ULTIPA_REQUEST.DeleteEdge(id=3))
# print(ret.toJSON())


# filter = FILTER.EqFilter(name='rank', value=12)
# ret = conn.deleteEdge(ULTIPA_REQUEST.DeleteEdge(filter=filter))
# print(ret.toJSON())

#
# ret = conn.listProperty(ULTIPA_REQUEST.GetProperty(type=DBType.DBNODE))
# print(ret.toJSON())
#
# ret = conn.listProperty(ULTIPA_REQUEST.GetProperty(type=DBType.DBEDGE))
# print(ret.toJSON())


# ret = conn.createProperty(ULTIPA_REQUEST.CreatProperty(type=DBType.DBNODE,name='test',property_type=PropertyTypeStr.PROPERTY_STRING))
# print(ret.toJSON())
#
# ret = conn.createProperty(ULTIPA_REQUEST.CreatProperty(type=DBType.DBEDGE,name='test',property_type=PropertyTypeStr.PROPERTY_STRING))
# print(ret.toJSON())


# ret = conn.dropProperty(ULTIPA_REQUEST.DropProperty(type=DBType.DBNODE,name='test'))
# print(ret.toJSON())


# ret = conn.dropProperty(ULTIPA_REQUEST.DropProperty(type=DBType.DBEDGE,name='test'))
# print(ret.toJSON())
#
# ret = conn.lte(ULTIPA_REQUEST.LTE(type=DBType.DBNODE,property='name'))
# print(ret.toJSON())

#
# ret = conn.lte(ULTIPA_REQUEST.LTE(type=DBType.DBEDGE,property='name'))
# print(ret.toJSON())

# ret = conn.ufe(ULTIPA_REQUEST.UFE(property='name',type=DBType.DBNODE))
# print(ret.toJSON())
#
# ret = conn.ufe(ULTIPA_REQUEST.UFE(property='name',type=DBType.DBEDGE))
# print(ret.toJSON())


# ret = conn.createIndex(ULTIPA_REQUEST.CreatIndex(node_property='test'))
# print(ret.toJSON())
# ret = conn.createIndex(ULTIPA_REQUEST.CreatIndex(edge_property='test'))
# print(ret.toJSON())



# ret = conn.createFullTextIndex(ULTIPA_REQUEST.CreateFullTextIndex(node_property='name',name='node_name'))
# print(ret.toJSON())

# ret = conn.showIndex()
# print(ret.toJSON())


# ret = conn.dropIndex(ULTIPA_REQUEST.DropIndex(node_property='test'))
# print(ret.toJSON())


# ret = conn.dropFullTextIndex(ULTIPA_REQUEST.DropFullTextIndex(name='node_name'))
# print(ret.toJSON())


# ret = conn.top()
# print(ret.toJSON())

# ret =  conn.kill(ULTIPA_REQUEST.Kill('1'))
# print(ret.toJSON())

# ret = conn.showTask(ULTIPA_REQUEST.ShowTask(limit=10))
# print(ret.toJSON())

# ret = conn.clearTask(ULTIPA_REQUEST.ClearTask(id=1,all=False))
# print(ret.toJSON())

# ret = conn.stopTask(ULTIPA_REQUEST.StopTask(id=1))
# print(ret.toJSON())



#################算法##############################
# ret = conn.listAlgo()
# print(ret.toJSON())
# ret = conn.algo_out_degree(ALGO_REQUEST.Out_Degree(node_id=1))
# print(ret.toJSON())

# ret = conn.algo_out_degree_all(ALGO_REQUEST.Out_Degree_All())
# print(ret.toJSON())

# ret = conn.algo_in_degree(ALGO_REQUEST.In_Degree(node_id=1))
# print(ret.toJSON())
# ret = conn.algo_in_degree_all(ALGO_REQUEST.In_Degree_All())
# print(ret.toJSON())

# ret = conn.algo_degree(ALGO_REQUEST.Degree(node_id=1))
# print(ret.toJSON())
#
# ret = conn.algo_degree_all(ALGO_REQUEST.Degree_All())
# print(ret.toJSON())

# ret = conn.algo_closeness(ALGO_REQUEST.Closeness(node_id=1))
# print(ret.toJSON())

# ret = conn.algo_out_closeness(ALGO_REQUEST.Out_Closeness(node_id=1))
# print(ret.toJSON())
#
# ret = conn.algo_in_closeness(ALGO_REQUEST.In_Closeness(node_id=1))
# print(ret.toJSON())

# ret = conn.algo_graph_centrality(ALGO_REQUEST.Graph_Centrality(node_id=1))
# print(ret.toJSON())

# ret = conn.algo_betweenness_centrality(ALGO_REQUEST.Betweenness_Centrality())
# print(ret.toJSON())


# ret = conn.algo_k_hop(ALGO_REQUEST.Khop(depth=3))
# print(ret.toJSON())


# ret = conn.algo_connected_component(ALGO_REQUEST.Connected_Component())
# print(ret.toJSON())

# ret = conn.algo_triangle_counting(ALGO_REQUEST.Triangle_Counting())
# print(ret.toJSON())

# ret = conn.algo_common_neighbours(ALGO_REQUEST.Common_neighbours(node_id1=12,node_id2=21))
# print(ret.toJSON())

# ret = conn.algo_subgraph(ALGO_REQUEST.Subgraph(node_ids=[12,21,1,123,33445,544]))
# print(ret.toJSON())

# ret = conn.algo_hyperANF(ALGO_REQUEST.HyperANF(loop_num=3,register_num=10))
# print(ret.toJSON())


# ret = conn.algo_knn(ALGO_REQUEST.Knn(node_id=12,node_property_names=['name','age'],top=50,target_property_name='name'))
# print(ret.toJSON())

# ret = conn.algo_k_core(ALGO_REQUEST.Kcore(k=10))
# print(ret.toJSON())


# ret = conn.algo_mst(ALGO_REQUEST.Mst(start_node_id=12,edge_property_name='rank'))
# print(ret.toJSON())

# ret = conn.algo_k_means(ALGO_REQUEST.K_Means(start_ids=[12,21,2,23,1],k=2,node_property_names=['name','age'],distance_type=0,loop_num=3))
# print(ret.toJSON())

# ret = conn.algo_clustering_coefficient(ALGO_REQUEST.Clustering_Coefficient(node_id=12))
# print(ret.toJSON())


# ret = conn.algo_page_rank(ALGO_REQUEST.Page_Rank(loop_num=3,damping=0.5))
# print(ret.toJSON())

# ret = conn.algo_sybil_rank(ALGO_REQUEST.Sybil_Rank(loop_num=3,sybil_num=3,trust_seeds=[12,21],total_trust=10))
# print(ret.toJSON())

# ret = conn.algo_lpa(ALGO_REQUEST.Lpa(loop_num=5,node_property_name='name'))
# print(ret.toJSON())

# ret = conn.algo_hanp(ALGO_REQUEST.Hanp(loop_num=3,edge_property_name='rank',node_property_name='name',m=1,delta=1.5))
# print(ret.toJSON())
#
# ret = conn.algo_louvain(ALGO_REQUEST.Louvain(phase1_loop_num=14,min_modularity_increase=0.5,edge_property_name='rank',visualization=True))
# print(ret.toJSON())

# ret = conn.algo_dv(ALGO_REQUEST.Dv(algo_name='louvain',id=7,top=10))
# print(ret.toJSON())


# ret = conn.algo_jaccard(ALGO_REQUEST.Jaccard(node_id1=12,top=10))
# print(ret.toJSON())

# ret = conn.algo_cosine_similarity(ALGO_REQUEST.Cosine_Similarity(node_id1=12,node_id2=21,node_property_names=['name','age']))
# print(ret.toJSON())


# ret = conn.algo_random_walk(ALGO_REQUEST.Random_Walk(walk_num=2,walk_length=3,edge_property_name='rank'))
# print(ret.toJSON())  # 服务器挂掉


# ret = conn.algo_random_walk_node2vec(ALGO_REQUEST.Random_Walk_Node2vec(walk_num=3,walk_length=2,p=0.1,q=0.1,edge_property_name='rank'))
# print(ret.toJSON())


# ret = conn.algo_random_walk_struc2vec(ALGO_REQUEST.Random_Walk_Stuc2vec(walk_num=3,walk_length=2,k=3,stay_probability=0.1))
# print(ret.toJSON())
# conn.lte(ULTIPA_REQUEST.LTE(property='rank',type=DBType.DBEDGE))

# ret = conn.algo_node2vec(ALGO_REQUEST.Node2vec(walk_num=2,loop_num=2,walk_length=2,p=0.1,q=0.1,context_size=2,dimension=10,learning_rate=0.3,min_learning_rate=0.3,sub_sample_alpha=0.001,resolution=2,neg_num=2,iter_num=2,min_frequency=0,edge_property_name='rank'))
# print(ret.toJSON())
#
# ret = conn.algo_line(ALGO_REQUEST.Line(edge_property_name='rank',dimension=2,resolution=3,start_alpha=0.0001,neg_num=1,total_sample=1,train_order=1))
# print(ret.toJSON())
#
# ret = conn.algo_struc2Vec(ALGO_REQUEST.Struc2Vec(walk_num=3,walk_length=2,k=2,stay_probability=0.2,context_size=0.5,dimension=10,learning_rate=0.025,min_learning_rate=0.001,sub_sample_alpha=0.001,resolution=10,neg_num=2,loop_num=3,min_frequency=3))
# print(ret.toJSON())


################权限和策略###########################
graphPrivilege = ULTIPA_REQUEST.GraphPrivilege(name='default',values=['QUERY'])
ret = conn.createPolicy(ULTIPA_REQUEST.CreatePolicy(name='sales',graph_privileges=graphPrivilege,))
print(ret.toJSON())


# graphPrivilege = ULTIPA_REQUEST.GraphPrivilege(name='default',values=['INSERT'])
# ret = conn.updatePolicy(ULTIPA_REQUEST.UpdatePolicy(name='sales',graph_privileges=graphPrivilege))
# print(ret.toJSON())


# ret = conn.deletePolicy(ULTIPA_REQUEST.DeletePolicy(name='sales4'))
# print(ret.toJSON())

# ret = conn.listPolicy()
# print(ret.toJSON())

# ret = conn.getPolicy(ULTIPA_REQUEST.GetPolicy(name='sales'))
# print(ret.toJSON())


# graphPrivilege = ULTIPA_REQUEST.GraphPrivilege(name='default',values=['INSERT'])
# ret = conn.grantPolicy(ULTIPA_REQUEST.GrantPolicy(username='test',graph_privileges=[graphPrivilege],policies=['sales']))
# print(ret.toJSON())

# graphPrivilege = ULTIPA_REQUEST.GraphPrivilege(name='default',values=['INSERT'])
# ret = conn.revokePolicy(ULTIPA_REQUEST.RevokePolicy(username='test',graph_privileges=[graphPrivilege],policies=['sales']))
# print(ret.toJSON())


# ret = conn.listPrivilege()
# print(ret.toJSON())


# ret = conn.createUser(ULTIPA_REQUEST.CreateUser(username='test',password='12345678'))
# print(ret.toJSON())

# ret = conn.getUser(ULTIPA_REQUEST.GetUser(username='test'))
# print(ret.toJSON())

# ret = conn.listGraph()
# print(ret.toJSON())

# ret = conn.updateUser(ULTIPA_REQUEST.UpdateUser(username='test',password='123456789'))
# print(ret.toJSON())

# ret = conn.deleteUser(ULTIPA_REQUEST.DeleteUser(username='test'))
# print(ret.toJSON())

# ret = conn.listGraph()
# print()


# ret = conn.listProperty()
# print(ret.toJSON())


# ret = conn.getProperty(ULTIPA_REQUEST.GetProperty(type=DBType.DBNODE))
# print(ret.data[0].toJSON())
# print(ret.toJSON())

# ret = conn.listUser()
# print(ret.toJSON())


# ret = conn.listGraph()
# print(ret.toJSON())

# ret = conn.createGraph(ULTIPA_REQUEST.CreateGraph(graphSetName='test1'))
# print(ret.toJSON())

# conn.listProperty()

# conn.truncate(request=ULTIPA_REQUEST.Truncate(ULTIPA.TruncateType.NODE))
# conn.truncate(request=ULTIPA_REQUEST.Truncate(ULTIPA.TruncateType.EDGE))
# conn.truncate(request=ULTIPA_REQUEST.Truncate(all=True))


# conn.insertNodesBulk()












