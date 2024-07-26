from ultipa import DBType
from ultipa.operate.base_extra import BaseExtra
from ultipa.types import ULTIPA_REQUEST, ULTIPA, ULTIPA_RESPONSE
from ultipa.structs.Property import Property
from ultipa.structs.Index import Index
from ultipa.utils import UQLMAKER, CommandList
from ultipa.configuration.RequestConfig import RequestConfig
from ultipa.structs.DBType import DBType
from ultipa.utils.convert import convertToIndex
from ultipa.utils.convert import convertToFullText

class IndexExtra(BaseExtra):

	'''
	Processing class that defines settings for index related operations.
	'''

	def showIndex(self,
				  requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.ResponseListIndex:
		'''
		Show all indice.

		Args:
			requestConfig: An object of RequestConfig class
			
		Returns:
			ResponseListIndex
		'''
		# if dbType != None:
		# 	command = dbType == DBType.DBNODE and CommandList.showNodeIndex or CommandList.showEdgeIndex
		# else:
		command = CommandList.showIndex
		uqlMaker = UQLMAKER(command=command, commonParams=requestConfig)
		res = self.UqlListSimple(uqlMaker=uqlMaker, isSingleOne=False)
		indexdata=convertToIndex(res=res,all=True)
		res.data=indexdata
		return res
	
	def showNodeIndex(self,requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.ResponseListIndex:
		'''
		Show all Node indice.

		Args:
			requestConfig: An object of RequestConfig class
			
		Returns:
			ResponseListIndex
		'''
		# res=self.showIndex(dbType=DBType.DBNODE,requestConfig=requestConfig)
		command = CommandList.showNodeIndex
		uqlMaker = UQLMAKER(command=command, commonParams=requestConfig)
		res = self.UqlListSimple(uqlMaker=uqlMaker, isSingleOne=False)
		indexdata=convertToIndex(res=res,all=False,dbtype=DBType.DBNODE)
		res.data=indexdata
		return res
	
	def showEdgeIndex(self,requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.ResponseListIndex:
		'''
		Show all Edge indice.

		Args:
			requestConfig: An object of RequestConfig class
			
		Returns:
			ResponseListIndex
		'''
		# res=self.showIndex(dbType=DBType.DBEDGE,requestConfig=requestConfig)
		command = CommandList.showEdgeIndex
		uqlMaker = UQLMAKER(command=command, commonParams=requestConfig)
		res = self.UqlListSimple(uqlMaker=uqlMaker, isSingleOne=False)
		indexdata=convertToIndex(res=res,all=False,dbtype=DBType.DBEDGE)
		res.data=indexdata
		return res
	

	def showFulltext(self,
					 requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.ResponseListIndex:
		'''
		Show all full-text indice.

		Args:
			requestConfig: An object of RequestConfig class
		Returns:
		
			ResponseListIndex
		'''
		# if dbType != None:
		# 	command = dbType == DBType.DBNODE and CommandList.showNodeFulltext or CommandList.showEdgeFulltext
		# else:
		command = CommandList.showFulltext
		uqlMaker = UQLMAKER(command=command, commonParams=requestConfig)
		res = self.UqlListSimple(uqlMaker=uqlMaker, isSingleOne=False)
		fulltextdata=convertToFullText(res=res)
		res.data=fulltextdata
		return res
	
	def showNodeFulltext(self,requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.ResponseListIndex:
		'''
		Show all full-text Node indice.

		Args:

			requestConfig: An object of RequestConfig class

		Returns:
		
			ResponseListIndex
		'''
		# res=self.showFulltext(dbType=DBType.DBNODE,requestConfig=requestConfig)
		command = CommandList.showNodeFulltext
		uqlMaker = UQLMAKER(command=command, commonParams=requestConfig)
		res = self.UqlListSimple(uqlMaker=uqlMaker, isSingleOne=False)
		fulltextdata=convertToFullText(res=res,all=False,dbtype=DBType.DBNODE)
		res.data=fulltextdata
		return res
	
	def showEdgeFulltext(self,requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.ResponseListIndex:
		'''
		Show all full-text Edge indice.

		Args:

			requestConfig: An object of RequestConfig class

		Returns:
		
			ResponseListIndex
		'''
		# res=self.showFulltext(dbType=DBType.DBEDGE,requestConfig=requestConfig)
		command = CommandList.showEdgeFulltext
		uqlMaker = UQLMAKER(command=command, commonParams=requestConfig)
		res = self.UqlListSimple(uqlMaker=uqlMaker, isSingleOne=False)
		fulltextdata=convertToFullText(res=res,all=False,dbtype=DBType.DBEDGE)
		res.data=fulltextdata
		return res
	
	

	def createIndex(self, dbType:DBType,propertyName:str,schemaName:str=None,
					requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		'''
		Create an index.

		Args:
			dbType: The DBType of data (DBNODE or DBEDGE)

			schemaName: The name of schema

			property: An object of Property class

			requestConfig: An object of RequestConfig class

		Returns:
			UltipaResponse
		'''

		command = dbType == DBType.DBNODE and CommandList.createNodeIndex or CommandList.createEdgeIndex
		# commandP = request.toString
		if schemaName:
			commandP = "@`%s`.`%s`" % (schemaName, propertyName)
		elif schemaName==None:
			commandP="@`*`.`%s`" % (propertyName)	
		uqlMaker = UQLMAKER(command=command, commandP=commandP, commonParams=requestConfig)
		res = self.uqlSingle(uqlMaker=uqlMaker)
		return res

	def createFulltext(self, dbType:DBType,schemaName:str,propertyName:str,fulltextName:str,
					   requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		'''
		Create a full-text index.

		Args:
			dbType: The DBType of data (DBNODE or DBEDGE)

			schemaName: The name of schema

			property: An object of Property class

			fulltextName: Name of the fulltext index

			requestConfig: An object of RequestConfig class

		Returns:
			UltipaResponse

		'''
		command = dbType == DBType.DBNODE and CommandList.createNodeFulltext or CommandList.createEdgeFulltext
		command1="@`%s`.`%s`" % (schemaName, propertyName)
		commandP = [command1,fulltextName]
		uqlMaker = UQLMAKER(command=command, commonParams=requestConfig)
		uqlMaker.setCommandParams(commandP=commandP)
		res = self.uqlSingle(uqlMaker=uqlMaker)
		return res

	def dropIndex(self, dbType:DBType,propertyName:str,schemaName:str=None,
					requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		'''
		Drop an index.

		Args:
			dbType: The DBType of data (DBNODE or DBEDGE)

			schemaName: The name of schema

			propertyName: The name of property

			requestConfig: An object of RequestConfig class

		Returns:
			UltipaResponse
		'''
		command = dbType == DBType.DBNODE and CommandList.dropNodeIndex or CommandList.dropEdgeIndex
		# commandP = request.toString
		if schemaName:
			commandP = "@`%s`.`%s`" % (schemaName, propertyName)
		elif schemaName==None:
			commandP="@`*`.`%s`" % (propertyName)

		uqlMaker = UQLMAKER(command=command, commandP=commandP, commonParams=requestConfig)
		res = self.uqlSingle(uqlMaker=uqlMaker)
		return res

	def dropFulltext(self,dbType:DBType,fulltextName:str,
					 requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		'''
		Drop a full-text index.

		Args:
			dbType: The DBType of data (DBNODE or DBEDGE)

			fulltextName: Name of the fulltext index

			requestConfig: An object of RequestConfig class

		Returns:
			UltipaResponse
		'''

		command = dbType == DBType.DBNODE and CommandList.dropNodeFulltext or CommandList.dropEdgeFulltext
		uqlMaker = UQLMAKER(command=command, commonParams=requestConfig)
		uqlMaker.setCommandParams(fulltextName)
		res = self.uqlSingle(uqlMaker=uqlMaker)
		return res
