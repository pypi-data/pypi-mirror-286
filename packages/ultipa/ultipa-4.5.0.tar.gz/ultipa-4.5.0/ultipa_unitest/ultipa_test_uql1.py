import datetime
import json
import time
import unittest

from ultipa import *
from ultipa.configuration.InsertConfig import InsertConfig
from ultipa.configuration.RequestConfig import RequestConfig
from ultipa.types.types import LoggerConfig
from ultipa.utils import UQLMAKER
from ultipa.utils.logger import LoggerConfig
from ultipa.utils.ultipa_datetime import wrapper, DateTimestamp, UTC
from ultipa_unitest import conn

class TestUltipaMethods(unittest.TestCase):

    @wrapper
    def test_uql_time1(self):
        conn.defaultConfig.defaultGraph="default"
        uql = "show().graph()"
        ret = conn.uql(uql)
        ret.Print()

    uqls = [
        # "find().nodes() as n return n{*} limit 20",
        # "n().e().n() as p return p{*} limit 4",
        # "profile n().e().n() as path return path",

    '''return [1,"2", ["a", 1],3, [4, ["b", 1]]] as p return p''',
    # "return null",
    # "return[null]",
    # "return [1, 2, 3]",
    # "return [1, null]",
    # "find().nodes() as nodes return collect(nodes)",
    # "find().edges() as edges return collect(edges)",
        # "return [1,2,3]",
        # "return [1, null]",
        # "find().nodes().limit(6) as nodes return collect(nodes)",
        # "find().edges().limit(6) as edges return collect(edges)",
        # "n().e().n().limit(6) as path return collect(path)",
        # "optional n(7).e().n(7) as path return path",
            ]

    @wrapper
    def test_uqls(self):
        conn.defaultConfig.defaultGraph = "miniCircle"
        for uql in self.uqls:
            ret = conn.uql(uql)
            ret.Print()
            # print(ret.toJSON())

    def test_uql(self):
        ret = conn.uql("top()")
        ret.Print()
        print(ret.toJSON())


    def test_nodes(self):
        data1 = [{'_id': '136', '_uuid': 136, 'age': 101, 'name': "insert_overwrite101"}]
        ret3 = conn.insertNode(ULTIPA_REQUEST.InsertNode(nodes=data1, schema='test_schema1'),
                               RequestConfig(graphName='test_node_create2233'))
        print(ret3.toJSON())
        print(ret3.status.code)

    def test_find_nodes(self):
        conn.defaultConfig.defaultGraph = "test_nodeList_0209"
        ret = conn.uql("find().nodes() return nodes{*}")
        print(ret.toJSON())

    def test_schema(self):
        conn.defaultConfig.defaultGraph = "test_nodeList_0210"
        ret = conn.uql("show().schema()")
        ret.Print()

    def test_template(self):
        conn.defaultConfig.defaultGraph = "miniCircle"
        uql = "n(47).e({})[*:2].n(73).limit(1) as path return pnodes(path)"
        ret = conn.uql(uql)
        print(ret.toJSON())
        ret.Print()

    def test_insert_nodes(self):
        str_name = "strList"
        int32_name = "int32List"
        # rows = [{str_name: ["test1", "test2", "test3"], int32_name: [1, 3, -5]},#
        # {str_name: ["test2", "test2", "test3"], int32_name: [2, 3, -5]},#
        # {str_name: ["test3", "test2", "test3"], int32_name: [3, 3, -5]},#
        # {str_name: ["test4", "test2", "test3"], int32_name: [4, 3, -5]},#
        # {str_name: ["test5", "test2", "test3"], int32_name: [5, 3, -5]},#
        # {str_name: ["test6", "test2", "test3"], int32_name: [6, 3, -5]}]
        ret = conn.insertNodesBatchAuto(nodes=[ULTIPA.EntityRow(schema="test_schema2",
                                                                values={str_name: ["test1", "test2", "test3"],
                                                                        int32_name: [1, 3, -5]}),
                                               ULTIPA.EntityRow(schema="test_schema2",
                                                                values={str_name: ["test1", "test2", "test3"],
                                                                        int32_name: [1, 3, -5]})
                                               ],
                                        config=InsertConfig(insertType=ULTIPA.InsertType.NORMAL,
                                                                           graphName='test_nodeList_0210'))
        print(ret.toJSON())



    def test_insert_edges(self):
        str_name = "strList"
        int32_name = "int32List"
        # rows = [{str_name: ["test1", "test2", "test3"], int32_name: [1, 3, -5]},#
        # {str_name: ["test2", "test2", "test3"], int32_name: [2, 3, -5]},#
        # {str_name: ["test3", "test2", "test3"], int32_name: [3, 3, -5]},#
        # {str_name: ["test4", "test2", "test3"], int32_name: [4, 3, -5]},#
        # {str_name: ["test5", "test2", "test3"], int32_name: [5, 3, -5]},#
        # {str_name: ["test6", "test2", "test3"], int32_name: [6, 3, -5]}]
        ret = conn.insertEdgesBatchAuto(edges=[ULTIPA.EntityRow(schema="test_schema2",
                                                                from_uuid=1,
                                                                to_uuid=2,
                                                                values={str_name: ["test1", "test2", "test3"],
                                                                        int32_name: [1, 3, -5]})],
                                        config=InsertConfig(insertType=ULTIPA.InsertType.NORMAL,
                                                                           graphName='test_nodeList_0210'))
        print(ret.toJSON())

    def testUql(self):
        uql = """find().nodes() limit 10 return nodes{*}"""
        # uql = """find().edges({_uuid < 10}) return collect(edges)"""
        # uql = """optional find().nodes(100000) as n optional n(n).e().n() as p RETURN p"""
        # uql = """n().e().n().limit(10) as p return collect(p)"""
        # uql = """find().nodes({@nodeSchemaList && _uuid in [3,5]}) return nodes.stringList"""
        # uql = """n({_uuid < 3} as n1).e().n() as paths GROUP BY n1 with collect(paths) as m return n1,m"""
        # uql = """find().nodes() as nodes order by nodes._uuid asc return collect(nodes.timestampList)"""
        uql = """n({_uuid == 47}).e({@response}).n({@account}).re({@response}).n({@account} as cards) with dedup(cards) as n return table(n.year,n._uuid) order by n.year, n._uuid desc limit 5"""
        uql = """find().nodes({_uuid < 5}) as n1 
call{with n1 khop().src(n1).depth(1) as n2 with collect(n2) as arrN2 n(n1).e({@response})[2].n({@account} as n3) with collect(n3) as arrN3
 return intersection(arrN2,arrN3),difference(arrN2,arrN3),listUnion(arrN2,arrN3),size(arrN3)} 
return intersection(arrN2,arrN3),difference(arrN2,arrN3),listUnion(arrN2,arrN3),size(arrN3)"""
        uql = "n({@account} as n1).e({@disagree}as e1).n() as paths return distinct(table(n1.name,e1.age)) limit 10"
        uql = "find().nodes({_uuid < 4}) as n1 with collect(n1) as arrN1 find().nodes({_uuid <> [5,9]}) as n2 with collect(n2) as arrN2 return intersection(arrN1,arrN2)"
        uql = "n({_id == 'CA001'}).e({@transfer})[2].n(as n).limit(10) as p order by n.balance desc return collect(p)"
        ret = conn.uql(uql, RequestConfig("playground_uql_manual_graph_1"))
        print(ret.toJSON())
        # print(ret.alias("m").asPathList().values[0][0])
        ret.Print()

    def testUql1(self):
        uqls= [
            # "stats()",
            # "show().property()",
            # "find().nodes() as n return n{*} limit 20",
            # "n().e().n() as p return p{*} limit 4",
            # "profile n().e().n() as path return path",
            # "n().e().n(_uuid==50) as p return p{*}",
            # "n().abc()",
            # '''return [1,"2", ["a", 1],3, [4, ["b", 1]]] as p return p''',
            # '''return "XXXX_ABCD" as p return p''',
            # '''return null''',
            # '''return [null]''',
            # '''return [1,2,3]''',
            # '''return [1, null, 2]''',
            # '''find().nodes().limit(6) as nodes return collect(nodes)''',
            # '''find().nodes() return nodes.string''',
            # '''find().nodes() return nodes.`[string]''',
            # '''find().nodes() return nodes{`[string]`}''',
            # '''find().nodes() as nodes return nodes._id, nodes._uuid, nodes.string, nodes.uint64, nodes.`[uint64]`''',
            # '''find().edges().limit(6) as edges return collect(edges)''',
            # '''n().e().n().limit(6) as path return collect(path)''',
            # '''n({_uuid < 3} as n1).e().n() as paths GROUP BY n1 with collect(paths) as m return n1,m''',
            # '''optional n(7).e().n(7) as path return path''',
            # '''find().edges({timestamp > "2020-08-22 13:02:09"}) as edges return edges{*} order by edges.timestamp''',
            # '''find().nodes({}) RETURN nodes.test_point''', # test_node_create9550
            # '''find().nodes({@account}) group by nodes.year RETURN table(nodes.year,count(nodes))''', # miniCircle
            '''find().nodes({@`nodeSchema3`}) as nodes return table(1,null,2,null,3,nodes.typeListDatetime[0],nodes.typeListTimestamp[0])''', # testCLI
            # '''n(47).e({})[*:2].n(73).limit(1) as path return pnodes(path)''',
              ]
        for uql in uqls:
            ret = conn.uql(uql, RequestConfig("testCLI"))
            # print(ret.alias("pnodes(path)").asNodeList().values)
            # ret.alias("n.strList").asNodes()
            ret.Print()
            # print(ret.toJSON())

    def test_uql_sucq(self):
        conn.defaultConfig.defaultGraph = 'test01'
        ret = conn.uql(
            'find().nodes({@TestSchema_01}) as nodes return nodes{datetime}')
        print(ret.toJSON())
        ret.Print()

    def test_uql_sucq1(self):
        conn.defaultConfig.defaultGraph = 'miniCircle329'
        ret = conn.uql(
            'khop().src(1).depth(1) as n1 order by n1._uuid desc return table(n1._uuid,n1.year) as table union all n(1).e().n({_uuid <15} as n1) order by n1._uuid desc return table(n1._uuid,n1.year) as table')
        print(ret.toJSON())
        ret.Print()

    def test_uql_maker(self):
        ret = UQLMAKER.PointFunction(1,1)
        print(ret)

    def test_time(self):
        # datetime1 = datetime.datetime(2022, 2, 12, 20, 59, 59, tzinfo=UTC())
        # print(datetime1.timestamp())
        # print(datetime1.strftime('%Y-%m-%d %H:%M:%S%z'))
        conn.defaultConfig.defaultGraph = 'miniCircle'
        ret = conn.uql('find().nodes({_uuid <> [10001, 10005]}) as n return n.set_1')
        # ret = conn.uql('find().nodes({_uuid <> [10001, 10005]}) as n return collect(n.name)')
        print(ret.toJSON())
        # ret.Print()

    def test_table(self):
        uql = 'n({@tag} as tag).re({@hasType}).n({@tagclass} as baseTagClass) ' \
              'where tag.name == "BasketballPlayer" || baseTagClass.name == "BasketballPlayer" with ' \
              'collect(distinct(tag._uuid)) as tags ' \
              'n(2175104).e({@knows}).n({@person} as friend).le({@hasCreator}).n({@comment} as comment).re({@replyOf}).n({@post}).re({@hasTag}).n(tags as tag1) ' \
              'group by friend with collect(distinct(tag1.name)) as tagNames,count(distinct(comment)) as replyCount order by replyCount desc,friend.original_id ' \
              'return table(friend.original_id,friend.firstName,friend.lastName,replyCount),tagNames limit 20'

        conn.defaultConfig.defaultGraph = 'ldbc_tiger_sf1_ic_fix_type'
        ret = conn.uql(uql)
        print(ret.toJSON())

    def test_show_schema(self):
        uql = "show().schema()"
        ret = conn.uql(uql)
        print(ret.toJSON())





