from typing import List
from ultipa.operate.base_extra import BaseExtra
from ultipa.types import ULTIPA_REQUEST, ULTIPA, ULTIPA_RESPONSE
from ultipa.utils import UQLMAKER, CommandList
from ultipa.configuration.RequestConfig import RequestConfig
from ultipa.structs.InsertType import InsertType
from ultipa.configuration.InsertConfig import InsertConfig
from ultipa.configuration.InsertRequestConfig import InsertRequestConfig
from ultipa.structs.Node import Node
from ultipa.utils.ufilter.new_ufilter import *

class NodeExtra(BaseExtra):
	'''
	Processing class that defines settings for node related operations.

	'''
	def searchNode(self, request: ULTIPA_REQUEST.SearchNode,
				   requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.ResponseSearchNode:
		'''
		Query for nodes.

		Args:
			request: An object of SearchNode class

			requestConfig: An object of RequestConfig class

		Returns:
			ResponseSearchNode

		'''

		uqlMaker = UQLMAKER(command=CommandList.nodes, commonParams=requestConfig)
		if request.id:
			uqlMaker.setCommandParams(request.id)
		elif request.filter:
			uqlMaker.setCommandParams(request.filter)
		uqlMaker.addParam('as', request.select.aliasName)
		uqlMaker.addParam("return", request.select)
		res = self.uqlSingle(uqlMaker)
		if res.status.code != ULTIPA.Code.SUCCESS:
			return res

		return res

	def insertNodes(self, nodes: List[Node], schemaName: str, config:InsertRequestConfig) -> ULTIPA_RESPONSE.ResponseInsertNode:
		'''
		Insert nodes.

		Args:
			nodes: List of nodes to be inserted

			schemaName: name of the Schema

			config: An object of InsertConfig classd

		Returns:
			ResponseInsertNode
		'''

		combined_values = []  # to combine values and id for insertion
		for node in nodes:
			node_dict = {}
			if node.id:
				node_dict["_id"] = node.id
			if node.uuid:
				node_dict["_uuid"]= node.uuid	
			node_dict.update(node.values)
			combined_values.append(node_dict)

		nodes=combined_values
		schemaName='@' + schemaName

		uqlMaker = UQLMAKER(command=CommandList.insert, commonParams=config)
		if config.insertType==InsertType.UPSERT:
			uqlMaker = UQLMAKER(command=CommandList.upsert, commonParams=config)
		if config.insertType==InsertType.OVERWRITE:
			uqlMaker.addParam('overwrite', "", required=False)
		if schemaName:
			uqlMaker.addParam('into', schemaName, required=False)

		uqlMaker.addParam('nodes', nodes)

		if config.silent==False:
			uqlMaker.addParam('as', "nodes")
			# uqlMaker.addParam('return', "nodes._uuid")
			uqlMaker.addParam('return', "nodes{*}")

		res = self.uqlSingle(uqlMaker)
		if res.status.code != ULTIPA.Code.SUCCESS:
			return res
		if config.silent==False:
			if len(res.aliases) > 0:
				res.data = res.items.get(res.aliases[0].alias).data
		return res

	def updateNodes(self, request: ULTIPA_REQUEST.UpdateNode,
				   requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		'''
		Update nodes.

		Args:
			request: An object of UpdateNode class

			requestConfig: An object of RequestConfig class

		Returns:
			UltipaResponse
		'''

		uqlMaker = UQLMAKER(command=CommandList.updateNodes, commonParams=requestConfig)
		if request.id:
			uqlMaker.setCommandParams(request.id)
		elif request.filter:
			uqlMaker.setCommandParams(request.filter)
		uqlMaker.addParam("set", request.values)
		uqlMaker.addParam("silent", request.silent)
		res = self.uqlSingle(uqlMaker)
		return res

	def deleteNodes(self,filter:str, config:InsertRequestConfig) -> ULTIPA_RESPONSE.ResponseDeleteNode:
		'''
		Delete nodes.

		Args:
			filter: An object of UltipaFilter class

			config: An object of InsertConfig class

		Returns:
			ResponseDeleteNode
		'''

		uqlMaker = UQLMAKER(command=CommandList.deleteNodes, commonParams=config)
		# if request.id:
		# 	uqlMaker.setCommandParams(request.id)
		if filter:
			uqlMaker.setCommandParams(filter)

		if config.silent==False:
			uqlMaker.addParam('as', "nodes")
			# uqlMaker.addParam('return', "nodes._uuid")	
			uqlMaker.addParam('return', "nodes{*}")
		res = self.uqlSingle(uqlMaker)

		if config.silent==False:
			if len(res.aliases) > 0:
				res.data = res.items.get(res.aliases[0].alias).data
		return res
