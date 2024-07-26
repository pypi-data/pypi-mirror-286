# -*- coding: utf-8 -*-
# @Time    : 2023/8/1 10:47
# @Author  : Ultipa
# @Email   : support@ultipa.com
# @File    : Graph.py
from ultipa.structs.BaseModel import BaseModel

class GraphSet(BaseModel):
    id: str
    name: str
    totalNodes: str
    totalEdges: str
    description: str
    status: str

    def __init__(self, name: str, id: str = None, totalNodes: str = None, 
                 totalEdges: str = None, description: str = None, status: str = None):
        self.id = id
        self.name = name
        self.totalNodes = totalNodes
        self.totalEdges = totalEdges
        self.description = description
        self.status = status



