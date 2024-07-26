# -*- coding: utf-8 -*-
# @Time    : 2023/8/26 11:44
# @Author  : Ultipa
# @Email   : support@ultipa.com
# @File    : test_create_subgraph.py
import json
import time
import unittest

from ultipa import *
from ultipa.types.types import LoggerConfig
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
        conn.defaultConfig.defaultGraph="miniCircle"
        ret = conn.uqlCreateSubgraph("n().e().n() as path return path{*} limit 10","test1")
        ret.Print()
        # print(ret.toJSON())