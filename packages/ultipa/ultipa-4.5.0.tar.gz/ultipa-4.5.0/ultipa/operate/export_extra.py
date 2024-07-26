from ultipa.operate.base_extra import BaseExtra
from ultipa.types import ULTIPA_REQUEST, ULTIPA_RESPONSE
from ultipa.configuration.RequestConfig import RequestConfig
from typing import Callable,List
from ultipa.structs.Node import Node
from ultipa.structs.Edge import Edge
class ExportExtra(BaseExtra):
	'''
		Processing class that defines settings for data exporting operation.
	'''

	def export(self, request: ULTIPA_REQUEST.Export,cb: Callable[[List[Node], List[Edge]], None],
			   requestConfig: RequestConfig = RequestConfig()) :
		'''
		Export data.

		Args:
			request: An object of Export class

			requestConfig: An object of RequestConfig class

		Returns:
			Stream
		'''
		self.exportData(request,cb,requestConfig)
		return 
