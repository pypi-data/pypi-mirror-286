# -*- coding: utf-8 -*-
# @Time    : 2023/4/4 15:02
# @Author  : Ultipa
# @Email   : support@ultipa.com
# @File    : test_uql_marker.py
from ultipa.utils.uql_marker import UQL, _replace

if __name__ == '__main__':
    ret = UQL.parse("'find().nodes({@test_node}) as n1                insert().overwrite().into(@test_node).nodes([{_uuid:n1._uuid,name:n1.name,age:n1.age+10}])'")
    # ret = UQL.parse_globle('alter().graph("test_graph125").set({"name": "test_graph126"})')
    print(_replace("nodes([{'point_name': 'point({latitude:1.1, longitude:1.5})'}])"))
    # print(ret.commands)

    # st = "nodes([{'point_name': 'point({latitude:1.1, longitude:1.5})'}])"
    #
    # st = re.sub(r"\'?\"?(point\([^)]*\))\'?\"?", , st)
    # print(st)
