import time

import json
from typing import Tuple

from ultipa.configuration.RequestConfig import RequestConfig
from ultipa.operate.base_extra import BaseExtra
from ultipa.structs import GraphSet
from ultipa.types import ULTIPA, ULTIPA_RESPONSE
from ultipa.utils import UQLMAKER, CommandList
from ultipa.utils.ResposeFormat import ResponseKeyFormat
from ultipa.utils.convert import convertToGraph

REPLACE_KEYS = {
	"graph": "name",
}


class GraphExtra(BaseExtra):

	'''
	Processing class that defines settings for graphset related operations.
	'''

	def uqlCreateSubgraph(self, uql: str, subGraphName: str, requestConfig: RequestConfig = RequestConfig()):
		ret = self.uql(uql, requestConfig)
		graphRet = self.getGraph(subGraphName)
		if graphRet.status.code != 0:
			self.createGraph(GraphSet(name=subGraphName))
			time.sleep(3)

	def showGraph(self, requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.ResponseListGraph:
		'''
		Acquire graphset list.

		Args:
			requestConfig: An object of RequestConfig class

		Returns:
			ResponseListGraph
		'''

		uqlMaker = UQLMAKER(command=CommandList.showGraph, commonParams=requestConfig)
		uqlMaker.setCommandParams("")
		res = self.UqlListSimple(uqlMaker=uqlMaker, responseKeyFormat=ResponseKeyFormat(keyReplace=REPLACE_KEYS))
		res.data=convertToGraph(res)
		return res

	def getGraph(self, graphName: str,
				 requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.ResponseGraph:
		'''
		Acquire a designated graphset.

		Args:
			graphName: The name of graphset

			requestConfig: An object of RequestConfig class

		Returns:
			UltipaResponse
		'''

		uqlMaker = UQLMAKER(command=CommandList.showGraph, commonParams=requestConfig)
		uqlMaker.setCommandParams(graphName)

		res = self.UqlListSimple(uqlMaker=uqlMaker, responseKeyFormat=ResponseKeyFormat(keyReplace=REPLACE_KEYS))
		res.data=convertToGraph(res)
		return res

	def createGraph(self, graph: GraphSet,
					requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		'''
		Create a graphset.

		Args:
			grpah: An object of Graph class

			requestConfig: An object of RequestConfig class

		Returns:
			UltipaResponse
		'''

		uqlMaker = UQLMAKER(command=CommandList.createGraph, commonParams=requestConfig)
		if graph.description:
			uqlMaker.setCommandParams([graph.name, graph.description])
		else:
			uqlMaker.setCommandParams(graph.name)
		res = self.uqlSingle(uqlMaker)
		return res

	def dropGraph(self, graphName: str,
				  requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		'''
		Drop a graphset.

		Args:
			graphName: The name of graphset

			requestConfig: An object of RequestConfig class

		Returns:
			UltipaResponse
		'''

		uqlMaker = UQLMAKER(command=CommandList.dropGraph, commonParams=requestConfig)
		uqlMaker.setCommandParams(graphName)
		res = self.uqlSingle(uqlMaker)
		return res

	def alterGraph(self, oldGraph: GraphSet, newGraph: GraphSet,
				   requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		'''
		Alter a graphset

		Args:
			oldGraphName: The orignal name of graphset

			newGraphName: The new name of graphset

			newDescription: The new description of graphset

			requestConfig: An object of RequestConfig class

		Returns:
			UltipaResponse
		'''

		requestConfig.graphName = oldGraph.name
		uqlMaker = UQLMAKER(command=CommandList.alterGraph, commonParams=requestConfig)
		uqlMaker.setCommandParams(oldGraph.name)
		data = {"name": newGraph.name}
		if newGraph.description is not None:
			data.update({'description': newGraph.description})
		uqlMaker.addParam("set", data)
		res = self.uqlSingle(uqlMaker)
		return res

	def hasGraph(self,graphName:str,requestConfig: RequestConfig = RequestConfig()) -> bool:
		'''
		Check if graph exists or not.

		Args:
			graphName: The name of graphset

			requestConfig: An object of RequestConfig class

		Returns:
			bool
		'''

		graphsdata=self.showGraph(requestConfig).data
		for graphs in graphsdata:
			if(graphs.name==graphName):
				return True
			
		return False	
	
	def createGraphIfNotExist(self, graph: GraphSet,
					requestConfig: RequestConfig = RequestConfig()) -> Tuple[bool,ULTIPA_RESPONSE.UltipaResponse] :
		'''
		Checks if graph exists or not, if graph does not exist then creates new.

		Args:
			graphName: The name of graphset

			requestConfig: An object of RequestConfig class

		Returns:
			bool
			UltipaResponse
		'''

		
		if(self.hasGraph(graph.name,requestConfig))==True:
			return [True,ULTIPA_RESPONSE.UltipaResponse()]
		
		else:
			res=self.createGraph(graph,requestConfig)
			return [False,res]
		



