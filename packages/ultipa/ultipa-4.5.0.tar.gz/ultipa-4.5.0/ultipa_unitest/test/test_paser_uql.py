# -*- coding: utf-8 -*-
# @Time    : 2022/6/30 10:58 上午
# @Author  : Ultipa
# @Email   : support@ultipa.com
# @File    : test_paser_uql.py
from ultipa.utils.uql_marker import UQL

cases = [
    {"uql": "find().nodes({(_id == 1 && c == 2)})"},
    {"uql": "show().graph()"},
    {"uql": '''show().graph("name")'''},
    {"uql": '''show().graph(name)'''},
    {"uql": '''create().graph("<name>", "<desc?>")'''},
    {"uql": '''algo(degree).params({})'''},
    {"uql": '''exec task algo(degree).params({})'''},
    {"uql": '''alert().node_property()'''},
    {"uql": '''n({_id == "C001"}).e().n({@card} as neighbors) find().nodes({_id == "C002"}) as C002 with neighbors, C002update().nodes({_id == neighbors._id && balance > C002.balance}).set({level: level + 1})'''},
    {"uql": "show().edge_schema(@amz).limit(100)"},
    {"uql": "show().edge_schema(@amz) limit 10"},
]
if __name__ == '__main__':
	for ca in cases:
		# print(ca.get("uql"))
		ret=UQL.parse(ca.get("uql"))
		print(ret.commands)
