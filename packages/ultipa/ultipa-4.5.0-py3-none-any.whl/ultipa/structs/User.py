# -*- coding: utf-8 -*-
# @Time    : 2024/05/14 11:47
# @Author  : Ultipa
# @Email   : support@ultipa.com
# @File    : User.py
from typing import List
from ultipa.structs.BaseModel import BaseModel


class User(BaseModel):
	'''
	    Data class for User.
	'''

	def __init__(self, username: str, create:str=None,graphPrivileges: dict=None,	systemPrivileges: List[str]=None,policies: List[str]=None,propertyPrivileges:dict=None):
		self.username = username
		self.create = create
		self.graphPrivileges = graphPrivileges
		self.systemPrivileges = systemPrivileges
		self.policies = policies
		self.propertyPrivileges=propertyPrivileges