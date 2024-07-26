# -*- coding: utf-8 -*-
# @Time    : 2024/05/17 10:56
# @Author  : Ultipa
# @Email   : support@ultipa.com
# @File    : Top.py
from ultipa.structs.BaseModel import BaseModel


class Top(BaseModel):
	'''
	    Data class for Top Processes.
	'''

	def __init__(self, process_id: str, process_uql: str,duration: str,status:str):
		self.process_id=process_id
		self.process_uql=process_uql
		self.duration=duration
		self.status=status