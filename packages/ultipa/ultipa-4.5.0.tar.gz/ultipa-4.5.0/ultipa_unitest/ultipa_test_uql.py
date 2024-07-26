import json
import time
import unittest

from ultipa import *
from ultipa.configuration.RequestConfig import RequestConfig
from ultipa.utils.logger import LoggerConfig
from ultipa.utils.ultipa_datetime import wrapper, DateTimestamp
from ultipa_unitest import conn

class TestUltipaMethods(unittest.TestCase):
    uqls = [
        "listUser()",  # tables
        "show().edge_property()",  #
        "show().node_property()",
        "find().nodes(1,2,3).select(*)",
        "find().edges(1,2,3).select(*)",
        "ab().src(12).dest(21).depth(5).limit(5).select(*)",
        "t().n(a).e().n(2).return(a.name,a.age)",
        "show().task()",
    ]
    def test_uqls(self):
        gname = ''
        ret = conn.stats()
        print(ret.toJSON())
        # self.assertEqual(ret.status.code,ULTIPA.Code.SUCCESS)
        # for i in self.uqls:
        #     ret = conn.uql(i)
        #     print(ret.toJSON())
        # self.assertEqual(ret.status.code,ULTIPA.Code.SUCCESS)
        # print(ret.toJSON())

    def test_uql_find_nodes(self):
        conn.defaultConfig.defaultGraph = 'amz'
        ret = conn.uql('''find().nodes({@default}) as nodes return nodes{*} limit 10''')
        print(ret.toJSON())
        # ret.Print()
        print(ret.alias("nodes").asNodes()[0].getUUID())
        print(ret.alias("nodes").asNodes()[0].getID())
        print(ret.alias("nodes").asNodes()[0].getValues())
        # print(ret.alias("nodes.@").asAttr().type)

        # ret =conn.uql('n({_uuid == 4}).e({@user_role} as edge).n({@role} as role) as path return path{}{*}')
        # print(ret.)
        # print(ret.toJSON())
        # print(ret.data.nodes[0].nodes[0].get('name'))
        # print(ret.data.toJSON())

    def test_uql_find_edges(self):
        conn.defaultConfig.defaultGraph="ultipa_www"
        # conn.defaultConfig.uqlLoggerConfig=LoggerConfig(logger=getlogger(name='test',filename='test.log',IsWriteToFile=True),isDetailed=False)
        ret = conn.uql('''
        n({@docs_tree.is_root=="true"} as book).e({@docs_tree})[:4].n(603 as docs).e({@docs_role}).n({@role} as roles) with docs,roles
n(docs as docs1).e({@docs_lang}).n({@lang} as lang) with book,docs1,roles,lang 
return book{*},docs1{*},roles{*},lang{*} limit -1''')
        print(ret.toJSON())
        aaa = ret.alias("book").asNodes()
        print(aaa)
        # print(ret.data.asEdges())


    def test_uql_find_path(self):
        conn.defaultConfig.defaultGraph='amz'
        # conn.defaultConfig.uqlLoggerConfig=LoggerConfig(logger=getlogger(name='test',filename='test.log',IsWriteToFile=True),isDetailed=False)
        ret = conn.uql('n().e().n() as edges return edges{*} limit 10')
        ret.Print()
        print(ret.toJSON())
        print(ret.alias("edges").asPaths()[0].getNodes()[0].schema)
        print(ret.alias("edges").asPaths()[0].getEdges())
        # print(ret.data)
        # print(ret.data.asEdges())


    def test_uql_array(self):
        conn.defaultConfig.defaultGraph='cpp_douban'
        # ret = conn.uql('find().nodes() as nodes group by nodes.year as y return y,count(nodes._id) limit 100')
        ret = conn.uql('n().e().n() as path return path{*} limit 1500')
        print(len(ret.data))
        print(len(ret.data[0].asPaths()))
        # for i in ret.data[0].asPaths():
        #
        #     print(i.toJSON())
        print(ret.toJSON())


    def test_uql_table_property(self):
        conn.defaultConfig.defaultGraph='miniCircle2'
        ret = conn.uql('show().property()')
        # print(ret.toJSON())
        # ret.toJSON()
        # ret.Print()
        for dat in ret.aliases:
            print(dat.alias)
        node = ret.alias("_nodeProperty")
        asProperties = node.asProperties()
        for p in asProperties:
            print(p.toJSON())




    def test_uql_table_index(self):
        conn.defaultConfig.defaultGraph='ct_test'
        ret = conn.uql('show().fulltext()')
        print(ret.toJSON())
        ret.Print()

    def test_uql_table_graph(self):
        conn.defaultConfig.defaultGraph='ct_test'
        ret = conn.uql('show().graph()')
        print(ret.get(0))

        # print(ret.toJSON())
        # ret.Print()

    def test_uql_table_schema(self):
        conn.defaultConfig.defaultGraph='ct_test'
        ret = conn.uql('show().schema()')
        print(ret.toJSON())
        ret.Print()
        # print(ret.alias("_nodeSchema").asSchemas()[0].total)
        # print(ret.alias("_nodeSchema").asSchemas()[0].name)




    def test_uql_paths(self):
        conn.defaultConfig.defaultGraph='test_with_9999'
        # ret = conn.uql('n().e().n() as paths return paths{*}{*}')
        ret = conn.uql('n({@account} as accounts).e().n({@card} as cards) group by accounts._id with accounts._id as accountID, collect(cards._id) as cardIDs, max(cards.level) as maxLV update().nodes({_id in cardIDs}).set({level: maxLV})')
        # ret.status.code

        print(ret.toJSON())
        # print(ret.data[0].asPaths()[0].getNodes()[0])
        # for i in ret.data.paths:
        #     ret1 = i.getNodes()
        #     for hj in ret1:
        #         for j in hj:
        #             print(j.getUUID())
                # print(hj.getID())
            # ret = i.getEdges()
            # print(ret)
        # print(ret.data.paths)
        # print(ret.data.asEdges())

    def test_table(self):
        ret = conn.uql('find().nodes({@default}) as nodes order by nodes._uuid desc limit 2 return table(nodes._id,nodes._uuid)',RequestConfig(graphName="ct_test"))
        # print(ret.data[0].asTable())
        ret.Print()
        # print(ret.statistics)
        # ret.get()
        print(ret.data[0].asNodes())
        # for i in ret.data.tables:
        #     print(i.toKV())
        # print(ret.data.tables)

    def test_attr(self):
        conn.defaultConfig.defaultGraph='ct_test'
        # ret = conn.uql('khop().src({_uuid == 1}).depth(1:1).edge_filter({@country}) as nodes return nodes{*}')
        # ret = conn.uql('n({_uuid == 28}).e({@role} as edge).n({@people} as people) as path return path{*}{*},people{*}')
        ret = conn.uql('find().nodes({@default}) as nodes order by nodes._uuid desc limit 2 return  nodes._uuid,nodes._id')
        print(ret.toJSON())
        ret.Print()

    def test_array(self):
        conn.defaultConfig.defaultGraph='miniCircle'
        # ret = conn.uql('khop().src({_uuid == 1}).depth(1:1).edge_filter({@country}) as nodes return nodes{*}')
        # ret = conn.uql('n({_uuid == 28}).e({@role} as edge).n({@people} as people) as path return path{*}{*},people{*}')
        ret = conn.uql('n({@account} as accounts).e().n({@movie.rating == 9} as maxRates) as paths return accounts._id, collect(maxRates._uuid) ,paths{*}')
        print(ret.aliases[0].alias)

        ret.Print()
        print(ret.toJSON())
    def test_array_1(self):
        conn.defaultConfig.defaultGraph='test_ab_path'
        ret = conn.uql('ab().src({_uuid == 11}).dest({_uuid == 15}).depth(4) as paths return paths{*}{*}')
        print(ret.toJSON())

    def test_algo(self):
        conn.defaultConfig.defaultGraph = 'multi_schema_test'
        ret = conn.uql('algo(louvain).params({"min_modularity_increase": 0.82, "phase1_loop_num": 9})',RequestConfig())
        conn.keepConnectionAlive()
        print(ret.toJSON())

    def test_uql_static(self):
        conn.defaultConfig.defaultGraph = 'test_transporter'
        ret = conn.uql("find().nodes({@default.age <= '22' || @default.name == '' || @default.age >= '22'}) as nodes return nodes{*} limit -1")
        print(ret.toJSON())

    def test_uql_no(self):
        conn.defaultConfig.defaultGraph = 'ultipa_www'
        ret = conn.uql(
            '''
            n({@version}).e().n({@docs_tree.status == 1} as book2).e().n({@lang.code == "en"}) with book2 as vbook
n(vbook).e().n({@docs_tree && is_root == "true"} as book1) with book1 as books
n(books).re({@docs_tree}).n(vbook).re({@docs_tree})[:2].n({@docs.status == 1 && @docs.type == "technical"} as n100) as path with path as docs_path, n100 as books2
n({books || vbook || books2}).e({@docs_role || @docs_tree_role}).n({@role.name in ["admin","public","viewer","sandBox","public"]}) as p with p as role_path
return docs_path{*}{*}, role_path{*},books
            '''
        )
        print(ret.toJSON())

    @wrapper
    def test_uql_schema(self):
        conn.defaultConfig.defaultGraph = 'miniCircle'
        ret = conn.uql("show().schema()")
        print(ret.toJSON())
        # ret.aliases
        print(ret.alias("_nodeSchema").asSchemas()[3].properties[0])



        # ret = conn.uql("show().property()")
        # print(ret.data[0].asProperty()[0])
        # print(ret.toJSON())
        #
        # ret = conn.uql("show().graph()")
        # print(ret.data[0].asGraph()[0])
        # print(ret.toJSON())



    @wrapper
    def test_uql_property(self):
        conn.defaultConfig.defaultGraph = 'miniCircle'
        ret1 = conn.showProperty()
        print(ret1.toJSON())
        ret = conn.uql("show().property()")
        print(ret.toJSON())

    @wrapper
    def test_uql_graph(self):
        conn.defaultConfig.defaultGraph = 'alimama_remote_by_id'
        ret1 = conn.showGraph()
        print(ret1.toJSON())
        ret = conn.uql("show().graph()")
        ret.Print()
        print(ret.data[0].asGraph()[0].name)

    @wrapper
    def test_uql_algos(self):
        # conn.defaultConfig.defaultGraph = 'alimama_remote_by_id'
        # ret1 = conn.showGraph()
        # print(ret1.toJSON())
        ret = conn.uql("show().algo()")
        ret.Print()
        # print(ret.toJSON())
        # print(ret.alias("_algoList").asAlgos()[0].toJSON())
        for algo in ret.alias("_algoList").asAlgos():
            print(algo.name)
            print(algo.version)
        #     print(algo.description)
        #     print(algo.parameters)
        #     print(algo.result_opt)

    @wrapper
    def test_uql_plan(self):
        conn.defaultConfig.defaultGraph = 'miniCircle'
        # conn.defaultConfig.setDefaultGraphName("default")
        # ret1 = conn.showGraph()
        # print(ret1.toJSON())
        ret = conn.uql("explain find().nodes() as n1 with n1 find().nodes() return n1{*},nodes{*}")
        ret.Print()
        print(ret.toJSON())


    def test_Print_table(self):
        conn.defaultConfig.defaultGraph = 'miniCircle'
        # ret = conn.uql("find().nodes({@company}) as n1 with n1 find().nodes({@company}) return n1{*},nodes{*} limit 10")
        # ret.Print()
        #
        # ret = conn.uql("find().edges({@relation}) as n1 with n1 find().edges({@relation}) return n1{*},edges{*} limit 10")
        # ret.Print()

        # ret = conn.uql("show().property()")
        # print(ret.toJSON())
        # ret.Print()
        #
        # ret = conn.uql("show().index()")
        # ret.Print()
        #
        # ret = conn.uql("show().graph()")
        # ret.Print()
        #
        ret = conn.uql("show().node_schema(@account)")
        # print(ret.toJSON())
        ret.Print()
        #
        # ret = conn.uql("show().algo()")
        # ret.Print()
        # #
        # ret = conn.uql("n(as nodes).e(as e).n().limit(10) return count(nodes),count(e)")
        # ret.Print()

    def test_Print_path(self):
        conn.defaultConfig.defaultGraph = 'amz'
        ret = conn.uql("n().e().n().e().n() as path return path{*} limit 10")
        print(ret.toJSON())
        print(ret.alias("path").asPaths()[0].nodeSchemas.get("amz").properties[0].name)
        ret.Print()

    def test_Print_array(self):
        conn.defaultConfig.defaultGraph = 'miniCircle'
        # ret = conn.uql("n({@account < 20} as user).e({@response})[2].n(79) return collect(distinct(user)) as arrUser",RequestConfig())
        ret = conn.uql("n({@account < 20} as user).e({@response})[2].n(79) return collect(distinct(user)) as arrUser", RequestConfig())
        ret.Print()

    def test_Print_array1(self):
        conn.defaultConfig.defaultGraph = 'miniCircle'
        ret = conn.uql("n({@account < 20} as user).e({@response})[2].n(79) return collect(distinct(user)) as arrUser",RequestConfig())
        # ret = conn.uql('''find().nodes() as n limit 10 return n{*}''',RequestConfig())
        print(ret.toJSON())
        ret.Print()
        # for i in ret.data:
        #     for j in i.asNodes():
        #         ret = j.values
        #         print(j.toJSON())
                # if isinstance(ret, DateTimestamp):
                #     ret: DateTimestamp = ret
                #     print(ret.timestamp)
                #     print(ret.datetime)
                #     print(ret.year)



    def test_uql_table(self):
        conn.defaultConfig.defaultGraph = 'uql_manual_graph_1'
        ret = conn.uql("find().nodes(6) return table(1,nodes.birthday)")
        ret.Print()


    def test_uql_insert(self):
        # conn.defaultConfig.defaultGraph = 'uql_manual_graph_1'
        # conn.defaultConfig.consistency=True
        for i in range(20):
            ret = conn.uql("find().nodes(6) return nodes{*}")
            time.sleep(5)
        # ret.Print()
        # print(ret.toJSON())
        #
    def test_uql_eq(self):
        conn.defaultConfig.defaultGraph = 'miniCircle'
        # ret = conn.uql("find().nodes() return nodes{*}")
        # ret.Print()
        # set
        ret = conn.uql("find().nodes({_uuid <> [10001, 10005]}) as n return n{*}")
        # set
        # ret = conn.uql("find().nodes({_uuid <> [10001, 10005]}) as n return n.set_1")
        # list
        # ret = conn.uql("find().nodes({_uuid <> [10001, 10005]}) as n return collect(n.set_1)")
        # list 
        # ret = conn.uql("find().nodes({_uuid < 10}) as nodes return nodes.int32List")
        ret.Print()


    @wrapper
    def test_uql_time(self):
        conn.defaultConfig.defaultGraph = "ultipa_www"
#         uql = '''
#         n({@version}).e().n({@docs_tree.status == 1} as book2).e().n({@lang.code == "en"}) with book2 as vbook
# n(vbook).e().n({@docs_tree && is_root == "true" && @docs_tree.status == 1} as book1) with book1 as books
# n(books).re({@docs_tree}).n(vbook).re({@docs_tree})[:3].n({@docs.status == 1 && @docs.type == "technical"|| @docs_tree} as n100) as path  with path as docs_path, n100 as books2
# n({books || vbook || books2}).e({@docs_role || @docs_tree_role}).n({@role.name in ["public"]}) as p with p as role_path
# return docs_path{*}, role_path{*},books
#         '''
#         uql = '''n(3241).e({@relationship} as e).n({@question.status in [0,1,2,3] && @question.lang=="en"} as questions) as path order by e._uuid DESC with questions,path skip 0 limit 10 n(questions).e().n({@tag || @user || @answer.status==1 && @answer.lang=="en"}) as path1 with questions,path,path1 return path{*},path1{*}
#         '''
        uql = '''n(3241).e({@relationship} as e).n({@question.status in [0,1,2,3] && @question.lang=="en"} as questions) as path order by e._uuid DESC with questions,path skip 10 limit 10 n(questions).e().n({@tag || @user || @answer.status==1 && @answer.lang=="en"}) as path1 with questions,path,path1 return path{*},path1{*}
        '''

        uql = "show().graph()"
        ret = conn.uql(uql)
        time.sleep(10)
        # print(ret.statistics.totalCost)
        # print(ret.toJSON())
        # print(ret.toJSON())
        ret.Print()

    @wrapper
    def test_uql_time1(self):
        conn.defaultConfig.defaultGraph = "ultipa_www"

        uql = "find().nodes({@user}) return nodes{*} limit 10"
        ret = conn.uql(uql)
        # print(ret.statistics.totalCost)
        print(ret.toJSON())
        # print(ret.toJSON())
        ret.Print()
        # time.sleep(21)

    @wrapper
    def test_uql_time1(self):
        conn.defaultConfig.defaultGraph="uql_manual_graph_2"
        uql = "optional find().nodes({age > 55}) as n return n{*}"
        ret = conn.uql(uql)
        # ret.Print()
        print(ret.toJSON())
        # li = ret.alias("collect(nodes.name)").asArray().elements
        # print(li)
        # print(ret.statistics.totalCost)
        # print(ret.toJSON())
        # print(ret.toJSON())
        # time.sleep(21)
    def test_graph_1(self):
        conn.defaultConfig.defaultGraph="miniCircle"
        uql = "n( as n1).re(as e).n(as n2) with toGraph(listUnion(collect(n1), collect(n2)), collect(e)) as graph return graph"
        ret = conn.uql(uql)
        ret1= ret.alias("graph").asGraph()
        print(ret1.node_table[0].getUUID())
        print(ret.toJSON())



