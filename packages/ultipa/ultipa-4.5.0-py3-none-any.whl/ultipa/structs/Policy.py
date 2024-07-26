# -*- coding: utf-8 -*-
# @Time    : 2024/05/14 11:47
# @Author  : Ultipa
# @Email   : support@ultipa.com
# @File    : Policy.py
from typing import List
from ultipa.structs.BaseModel import BaseModel


class Policy(BaseModel):
	'''
	    Data class for Policy.
	'''

	def __init__(self, name: str, graphPrivileges: dict = None, systemPrivileges: List[str] = None, propertyPrivileges:dict=None,
				 policies: List[str] = None):
		self.name = name
		self.graphPrivileges = graphPrivileges
		self.systemPrivileges = systemPrivileges
		self.propertyPrivileges=propertyPrivileges
		self.policies = policies