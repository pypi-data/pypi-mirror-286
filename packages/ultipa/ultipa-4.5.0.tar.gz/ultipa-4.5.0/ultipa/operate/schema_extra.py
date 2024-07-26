from ultipa.configuration.RequestConfig import RequestConfig
from ultipa.operate.base_extra import BaseExtra
from ultipa.structs import Schema
from ultipa.structs import DBType
from ultipa.types import ULTIPA, ULTIPA_REQUEST, ULTIPA_RESPONSE
from ultipa.utils import UQLMAKER, CommandList
from ultipa.utils.ResposeFormat import ResponseKeyFormat
from typing import Tuple
from ultipa.operate.property_extra import PropertyExtra
from ultipa.structs.Property import Property

BOOL_KEYS = ["index", "lte"]
REPLACE_KEYS = {
	"name": "schemaName",
	"type": "propertyType",
}


class SchemaExtra(BaseExtra):
	'''
		Prcessing class that defines settings for schema related operations.
	'''

	def createSchema(self, schema: Schema, isCreateProperties:bool = False,
					 requestConfig: RequestConfig = RequestConfig())->ULTIPA_RESPONSE.UltipaResponse:
		'''
		Create a schema.

		Args:
			schema: An object of Schema class

			requestConfig: An object of RequestConfig class

		Returns:
			UltipaResponse

		'''

		command = schema.DBType == DBType.DBNODE and CommandList.createNodeSchema or CommandList.createEdgeSchema
		commandP = [f"`{schema.name}`"]
		if schema.description:
			commandP.append(schema.description)
		uqlMaker = UQLMAKER(command=command, commonParams=requestConfig)
		uqlMaker.setCommandParams(commandP=commandP)
		res = self.uqlSingle(uqlMaker=uqlMaker)
	
		if isCreateProperties:
			if schema.properties:
				for prop in schema.properties:
					try:
						res1 = PropertyExtra.createProperty(self, dbType=schema.DBType, schemaName=schema.name, prop=prop)
					except Exception as e:
						print("An error occurred while creating property:", prop.name, "Error:", e)		
		return res


	def showSchema(self,
				   requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.ResponseListSchema:
		'''
		Show schema(s).

		Args:			
			requestConfig: An object of RequestConfig class

		Returns:
			ResponseListSchema

		'''

		command = CommandList.showSchema		
		commandP = ''

		uqlMaker = UQLMAKER(command=command, commandP=commandP, commonParams=requestConfig)
		res = self.uqlSingle(uqlMaker)
		schemalist=[]
		nodeschemas=res.alias("_nodeSchema").asSchemas()
		edgeschemas=res.alias("_edgeSchema").asSchemas()
		schemalist.append(nodeschemas)
		schemalist.append(edgeschemas)
		res.items=schemalist
		return res
	


	def showNodeSchema(self,requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.ResponseListSchema:
		'''
		Show Nodeschema(s).

		Args:			
			requestConfig: An object of RequestConfig class

		Returns:
			ResponseListSchema

		'''

		command=CommandList.showNodeSchema
		commandp=''
		# 	if schemaName:
		# 		commandP = '@' + schemaName
		# 	else:
		# 		commandP = ''
		# else:
		# 	command = CommandList.showSchema
		# 	commandP = ''
		uqlMaker = UQLMAKER(command=command,commandP=commandp, commonParams=requestConfig)
		res = self.uqlSingle(uqlMaker)
		res.items = res.alias("_nodeSchema").asSchemas()
		return res
	
	def showEdgeSchema(self,requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.ResponseListSchema:
		'''
		Show Edgeschema(s).

		Args:			
			requestConfig: An object of RequestConfig class

		Returns:
			ResponseListSchema

		'''

		command=CommandList.showEdgeSchema
		commandp=''
		# 	if schemaName:
		# 		commandP = '@' + schemaName
		# 	else:
		# 		commandP = ''
		# else:
		# 	command = CommandList.showSchema
		# 	commandP = ''

		# uqlMaker = UQLMAKER(command=command, commandP=commandP, commonParams=requestConfig)
		uqlMaker = UQLMAKER(command=command,commandP=commandp, commonParams=requestConfig)
		res = self.uqlSingle(uqlMaker)
		res.items = res.alias("_edgeSchema").asSchemas()
		return res


	def alterSchema(self, schema:Schema,newSchema:Schema,
					requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		'''
		Alter schema.

		Args:
			schema: An object of schema class(to be altered)
			newSchema: An object of schema class

		Returns:
			 UltipaResponse

		'''
		command = schema.DBType == DBType.DBNODE and CommandList.alterNodeSchema or CommandList.alterEdgeSchema
		# commandP = '@' + schema.name
		commandP="@`%s`" % (schema.name)
		update_dict = {}
		if newSchema.name:
			update_dict.setdefault('name', newSchema.name)
		if newSchema.description:
			update_dict.update({'description': newSchema.description})
		uqlMaker = UQLMAKER(command=command, commandP=commandP, commonParams=requestConfig)
		uqlMaker.addParam("set", update_dict)
		res = self.uqlSingle(uqlMaker=uqlMaker)
		return res

	def dropSchema(self, schema:Schema,
				   requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		'''
		Drop schema.

		Args:
			schema: An object of schema class

		Returns:
			 UltipaResponse

		'''

		command = schema.DBType == DBType.DBNODE and CommandList.dropNodeSchema or CommandList.dropEdgeSchema
		# commandP = '@' + schema.name
		commandP="@`%s`" % (schema.name)

		uqlMaker = UQLMAKER(command=command, commandP=commandP, commonParams=requestConfig)
		res = self.uqlSingle(uqlMaker=uqlMaker)
		return res
	
	def getSchema(self, schemaName: str, dbType: DBType,
				 requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.ResponseSchema:
		'''
		Acquire a designated Schema.

		Args:
			schemaName: The name of Schema
			
			dbType:The DBType of data (DBNODE or DBEDGE)

			requestConfig: An object of RequestConfig class

		Returns:
			ResponseSchema
		'''

		
		if dbType != None:
			if dbType == DBType.DBNODE:
				command = CommandList.showNodeSchema
			elif dbType == DBType.DBEDGE:
				command = CommandList.showEdgeSchema

			if schemaName:
				commandP="@`%s`" % (schemaName)


		uqlMaker = UQLMAKER(command, commandP=commandP,commonParams=requestConfig)

		res = self.uqlSingle(uqlMaker=uqlMaker)
		if res.status.code==ULTIPA.Code.SUCCESS:
			if dbType==DBType.DBNODE:
				res.items = res.alias("_nodeSchema").asSchemas()[0]
			else:
				res.items = res.alias("_edgeSchema").asSchemas()[0]
		return res	
	

	def getNodeSchema(self, schemaName: str,
				 requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.ResponseSchema:
		'''
		Acquire a designated Node Schema.

		Args:
			schemaName: The name of Schema
			requestConfig: An object of RequestConfig class

		Returns:
			ResponseSchema
		'''

		
		command=CommandList.showNodeSchema

		if schemaName:
			commandP="@`%s`" % (schemaName)


		uqlMaker = UQLMAKER(command, commandP=commandP,commonParams=requestConfig)

		res = self.uqlSingle(uqlMaker=uqlMaker)
		res.items = res.alias("_nodeSchema").asSchemas()[0]
		return res
		
	
	def getEdgeSchema(self, schemaName: str,
				 requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.ResponseSchema:
		'''
		Acquire a designated Edge Schema.

		Args:
			schemaName: The name of Schema
			requestConfig: An object of RequestConfig class

		Returns:
			ResponseSchema
		'''

		
		command=CommandList.showEdgeSchema

		if schemaName:
			commandP="@`%s`" % (schemaName)


		uqlMaker = UQLMAKER(command, commandP=commandP,commonParams=requestConfig)

		res = self.uqlSingle(uqlMaker=uqlMaker)
		res.items = res.alias("_edgeSchema").asSchemas()[0]
		return res
	

	def createSchemaIfNotExist(self, schema: Schema,
					 requestConfig: RequestConfig = RequestConfig())->Tuple [bool,ULTIPA_RESPONSE.UltipaResponse]:
		'''
		Create a schema if schema does not exist.

		Args:
			schema: An object of Schema class

			requestConfig: An object of RequestConfig class

		Returns:
			UltipaResponse

		'''
		check=self.getSchema(schemaName=schema.name,dbType=schema.DBType)
		if check.status.code==ULTIPA.Code.SUCCESS:
			return [True,ULTIPA_RESPONSE.UltipaResponse()]

		elif check.status.code==ULTIPA.Code.FAILED:
			res=self.createSchema(schema=schema,isCreateProperties=True,requestConfig=requestConfig)
			return [False,res]


	def getProperty(self, dbType: DBType, propertyName: str, schemaName: str , 
					requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.ResponseProperty:
		'''
		Get a property.

		Args:
			dbType: The DBType of data (DBNODE or DBEDGE)

			schemaName: The name of schema

			propertyName: The name of the Property

			requestConfig: An object of RequestConfig class

		Returns:
			Response

		'''
		res= self.getSchema(schemaName=schemaName,dbType=dbType,requestConfig=requestConfig)
		properties=res.items.properties
		for property in properties:
			if property.name==propertyName:
				return property
		return None	
	
	def getNodeProperty(self,propertyName: str, schemaName: str , 
					requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.ResponseProperty:
		'''
		Get a Node property.

		Args:
			schemaName: The name of schema

			propertyName: The name of the Property

			requestConfig: An object of RequestConfig class

		Returns:
			Response

		'''
		res=self.getProperty(propertyName=propertyName,schemaName=schemaName,dbType=DBType.DBNODE,requestConfig=requestConfig)
		return res
	
	def getEdgeProperty(self,propertyName: str, schemaName: str , 
					requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.ResponseProperty:
		'''
		Get an Edge property.

		Args:
			schemaName: The name of schema

			propertyName: The name of the Property

			requestConfig: An object of RequestConfig class

		Returns:
			Response

		'''
		res=self.getProperty(propertyName=propertyName,schemaName=schemaName,dbType=DBType.DBEDGE,requestConfig=requestConfig)
		return res
	
	def createPropertyIfNotExist(self, dbType:DBType, schemaName:str, prop:Property,
					 requestConfig: RequestConfig = RequestConfig())->Tuple [bool,ULTIPA_RESPONSE.ResponseProperty]:
		'''
		Create a schema if schema does not exist.

		Args:
			schema: An object of Schema class

			requestConfig: An object of RequestConfig class

		Returns:
			Bool
			ResponseGetProperty

		'''

		res=self.getProperty(dbType=dbType,propertyName=prop.name,schemaName=schemaName,requestConfig=requestConfig)
		if res!= None:
			return[True,ULTIPA_RESPONSE.ResponseProperty()]
		if res == None:
			newprop=PropertyExtra.createProperty(self,dbType=dbType,schemaName=schemaName,prop=prop)
			return [False, newprop]