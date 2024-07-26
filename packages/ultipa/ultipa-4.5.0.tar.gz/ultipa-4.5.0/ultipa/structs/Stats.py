# -*- coding: utf-8 -*-
# @Time    : 2024/05/17 10:56
# @Author  : Ultipa
# @Email   : support@ultipa.com
# @File    : Stats.py
from ultipa.structs.BaseModel import BaseModel


class Stats(BaseModel):
	'''
	    Data class for Statistics.
	'''

	def __init__(self, cpuUsage: str, memUsage: str,company: str,cpuCores: str,expiredDate: str,serverType: str,version: str):
		self.cpuUsage=cpuUsage
		self.memUsage=memUsage
		self.company=company
		self.cpuCores=cpuCores
		self.expiredDate=expiredDate
		self.serverType=serverType
		self.version=version
	
	
	
	
	
	
	