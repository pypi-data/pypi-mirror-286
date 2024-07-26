from ultipa.operate.base_extra import BaseExtra
from ultipa.structs import DBType
from ultipa.types import ULTIPA_REQUEST, ULTIPA, ULTIPA_RESPONSE
from ultipa.utils import UQLMAKER, CommandList
from ultipa.structs.Property import Property
from ultipa.configuration.RequestConfig import RequestConfig

class LteUfeExtra(BaseExtra):

	'''
	Processsing class that defines settings for LTE and UFE related operations.
	'''

	def lte(self, dbType:DBType, propertyName:str,schemaName:str=None, 
			requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		'''
		Load properties to memory (LTE).

		Args:
			dbType: The DBType of data (DBNODE or DBEDGE)

			schemaName: The name of schema

			property: An object of Property class

			requestConfig: An object of RequestConfig class

		Returns:
			UltipaResponse
		'''

		command = dbType == DBType.DBNODE and CommandList.lteNode or CommandList.lteEdge
		uqlMaker = UQLMAKER(command=command, commonParams=requestConfig)
		if schemaName:
			commandP = "@`%s`.`%s`" % (schemaName, propertyName)
		elif schemaName==None:
			commandP="@`*`.`%s`" %(propertyName)	
		uqlMaker.setCommandParams(commandP=commandP)
		res = self.uqlSingle(uqlMaker=uqlMaker)
		return res

	def ufe(self, dbType:DBType, propertyName:str, schemaName:str=None,
			requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		'''
		Unload properties from memory (UFE).

		Args:
			dbType: The DBType of data (DBNODE or DBEDGE)

			schemaName: The name of schema

			property: An object of Property class

			requestConfig: An object of RequestConfig class

		Returns:
			UltipaResponse
		'''

		command = dbType == DBType.DBNODE and CommandList.ufeNode or CommandList.ufeEdge
		uqlMaker = UQLMAKER(command=command, commonParams=requestConfig)
		if schemaName:
			commandP = "@`%s`.`%s`" % (schemaName, propertyName)
		elif schemaName==None:
			commandP="@`*`.`%s`" %(propertyName)	
		uqlMaker.setCommandParams(commandP=commandP)
		res = self.uqlSingle(uqlMaker=uqlMaker)
		return res
