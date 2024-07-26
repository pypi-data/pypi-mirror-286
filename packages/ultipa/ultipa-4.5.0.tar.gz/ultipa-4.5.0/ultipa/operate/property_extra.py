from ultipa.configuration.RequestConfig import RequestConfig
from ultipa.operate.base_extra import BaseExtra
from ultipa.structs import DBType
from ultipa.structs.Property import Property
from ultipa.types import ULTIPA, ULTIPA_RESPONSE
from ultipa.utils import UQLMAKER, CommandList
from ultipa.utils.ResposeFormat import ResponseKeyFormat
from ultipa.utils.propertyUtils import getPropertyTypesDesc
from typing import Tuple

BOOL_KEYS = ["index", "lte"]
REPLACE_KEYS = {
	"name": "propertyName",
	"type": "propertyType",
}


class PropertyExtra(BaseExtra):
	'''
	Processing class that defines settings for property related operations.
	'''

	# def listProperty(self, requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.ResponseListProperty:
	# 	'''
	# 	List all properties.

	# 	Args:
	# 		requestConfig: An object of RequestConfig class

	# 	Returns:
	# 		ResponseListProperty

	# 	'''
	# 	return self.showProperty(requestConfig)

	def showProperty(self, dbType: DBType, schemaName:str=None , requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.ResponseListProperty:
		'''
		Show all Node or Edge Schema properties.

		Args:
			dbType: The DBType of data (DBNODE or DBEDGE)

			schema: The name of schema

			requestConfig: An object of RequestConfig class

		Returns:
			ResponseListProperty

		'''
		if dbType != None:
			if dbType == DBType.DBNODE:
				command = CommandList.showNodeProperty
			elif dbType == DBType.DBEDGE:
				command = CommandList.showEdgeProperty
			else:
				command = CommandList.showNodeProperty
			if schemaName:
				commandp = ['@' + f"`{schemaName}`"]
			else:
				commandp = ''
				
		uqlMaker = UQLMAKER(command=command, commonParams=requestConfig)
		uqlMaker.setCommandParams(commandP=commandp)
		# res = self.UqlListSimple(uqlMaker=uqlMaker,
		# 						 responseKeyFormat=ResponseKeyFormat(boolKeys=BOOL_KEYS),
		# 						 isSingleOne=False)
		res=self.uqlSingle(uqlMaker=uqlMaker)
		if dbType==DBType.DBNODE:
			res.items=res.alias("_nodeProperty").asProperties()
		else:
			res.items=res.alias("_edgeProperty").asProperties()	
		return res
	

	def showNodeProperty(self, schemaName:str=None , requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.ResponseListProperty:
		'''
		Show all Node Schema properties.

		Args:
			schemaName: The name of schema

			requestConfig: An object of RequestConfig class

		Returns:
			ResponseListProperty

		'''
		res=self.showProperty(schemaName=schemaName,dbType=DBType.DBNODE,requestConfig=requestConfig)
		return res
	
	def showEdgeProperty(self, schemaName:str=None , requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.ResponseListProperty:
		'''
		Show all Edge Schema properties.

		Args:
			schemaName: The name of schema

			requestConfig: An object of RequestConfig class

		Returns:
			ResponseListProperty

		'''
		
		res=self.showProperty(schemaName=schemaName,dbType=DBType.DBEDGE,requestConfig=requestConfig)
		return res


	def createProperty(self, dbType: DBType, schemaName: str, prop: Property,
					   requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		'''
		Create a property.

		Args:
			dbType: The DBType of data (DBNODE or DBEDGE)

			schema: The name of schema

			prop:  An object of Property class

			requestConfig: An object of RequestConfig class

		Returns:
			UltipaResponse

		'''
		command = dbType == DBType.DBNODE and CommandList.createNodeProperty or CommandList.createEdgeProperty
		commandP = ["@" + f"`{schemaName}`", f"`{prop.name}`",
					getPropertyTypesDesc(prop.type, prop.subTypes)]

		if prop.description:
			commandP.append(prop.description)
		uqlMaker = UQLMAKER(command=command, commonParams=requestConfig)
		uqlMaker.setCommandParams(commandP=commandP)
		res = self.uqlSingle(uqlMaker)
		return res

	def dropProperty(self, dbType: DBType, schemaName: str, propertyName: str,
					 requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		'''
		Drop a property.

		Args:
			dbType: The DBType of data (DBNODE or DBEDGE)

			schema: The name of schema

			property: The name of property

			requestConfig: An object of RequestConfig class

		Returns:
			UltipaResponse

		'''
		command = dbType == DBType.DBNODE and CommandList.dropNodeProperty or CommandList.dropEdgeProperty
		commandP = "@`%s`.`%s`" % (schemaName, propertyName)
		uqlMaker = UQLMAKER(command=command, commonParams=requestConfig)
		uqlMaker.setCommandParams(commandP=commandP)
		res = self.uqlSingle(uqlMaker)
		return res

	def alterProperty(self, dbType: DBType, property:Property, newProperty:Property,
					  requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		'''
		Alter a property.

		Args:
			dbType: The DBType of data (DBNODE or DBEDGE)

			property: The name of property

			newProperty: The new name of property

			requestConfig: An object of RequestConfig class

		Returns:
			UltipaResponse

		'''
		command = dbType == DBType.DBNODE and CommandList.alterNodeProperty or CommandList.alterEdgeProperty
		commandP = "@`%s`.`%s`" % (property.schema, property.name)
		update_dict = {}
		if newProperty.name:
			update_dict.setdefault('name', newProperty.name)
		if newProperty.description:
			update_dict.update({'description': newProperty.description})
		uqlMaker = UQLMAKER(command=command, commonParams=requestConfig)
		uqlMaker.setCommandParams(commandP)
		uqlMaker.addParam("set", update_dict)
		res = self.uqlSingle(uqlMaker)
		return res
	



		
