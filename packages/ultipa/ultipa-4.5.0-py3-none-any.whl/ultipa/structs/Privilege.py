# -*- coding: utf-8 -*-
# @Time    : 2024/05/14 11:47
# @Author  : Ultipa
# @Email   : support@ultipa.com
# @File    : Privilege.py
from typing import List
from ultipa.structs.BaseModel import BaseModel


class Privilege(BaseModel):
	'''
	    Data class for Privilege.
	'''

	def __init__(self, 	graphPrivileges: List[str],systemPrivileges: List[str]):
		self.graphPrivileges=graphPrivileges
		self.systemPrivileges=systemPrivileges