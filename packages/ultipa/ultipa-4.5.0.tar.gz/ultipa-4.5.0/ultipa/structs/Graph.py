# -*- coding: utf-8 -*-
# @Time    : 2023/11/28 11:50
# @Author  : Ultipa
# @Email   : support@ultipa.com
# @File    : Graph.py
from typing import List

from ultipa.structs.Node import Node
from ultipa.structs.Edge import Edge
from ultipa.structs.BaseModel import BaseModel

class Graph:
	node_table:List[Node] = None
	edge_table:List[Edge] = None
	def __init__(self, node_table, edge_table):
		self.node_table = node_table
		self.edge_table = edge_table


class GraphAlias(BaseModel):
	alias:str=None
	graph:Graph=None

	def __init__(self, alias, graph):
		self.alias = alias
		self.graph = graph