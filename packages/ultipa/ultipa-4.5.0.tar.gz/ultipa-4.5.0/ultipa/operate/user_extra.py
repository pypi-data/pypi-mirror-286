from ultipa.operate.base_extra import BaseExtra
from ultipa.utils import UQLMAKER, CommandList
from ultipa.types import ULTIPA_REQUEST, ULTIPA_RESPONSE
from ultipa.utils.errors import ParameterException
from ultipa.utils.format import FormatType
from ultipa.utils.ResposeFormat import ResponseKeyFormat
from ultipa.configuration.RequestConfig import RequestConfig
from ultipa.proto import ultipa_pb2
from ultipa.connection.clientType import ClientType
from ultipa.types import ULTIPA, ULTIPA_REQUEST, ULTIPA_RESPONSE
from ultipa.utils.convert import convertToUser

JSONSTRING_KEYS = ["graphPrivileges", "systemPrivileges", "policies", "policy", "privilege"]
formatdata = ['graph_privileges']


class UserExtra(BaseExtra):
	'''
		Processing class that defines settings for user related operations.
	'''

	def _GRPATH_PRIVILEGES_DATA_FORMAT(self, obj):
		if isinstance(obj.get('graph_privileges'), list):
			resr = FormatType.graphPrivileges(obj.get('graph_privileges'))
			return resr
		else:
			return '[]'

	def showUser(self,
				 requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.ResponseListUser:
		'''
		Show user list.

		Args:
			requestConfig: An object of RequestConfig class

		Returns:
			ResponseListUser

		'''

		uqlMaker = UQLMAKER(command=CommandList.showUser, commonParams=requestConfig)
		res = self.UqlListSimple(uqlMaker=uqlMaker,
								 responseKeyFormat=ResponseKeyFormat(jsonKeys=JSONSTRING_KEYS, dataFormat=formatdata))
		if len(res.data)>0:
			res.data=convertToUser(res)
		return res

	def getUser(self, userName:str,
				requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.ResponseUser:
		'''
		Get a designated user.

		Args:
			username: The name of user

			requestConfig: An object of RequestConfig class

		Returns:
			ResponseUser

		'''

		uqlMaker = UQLMAKER(command=CommandList.getUser, commonParams=requestConfig)
		uqlMaker.setCommandParams(userName)
		res = self.UqlListSimple(uqlMaker=uqlMaker,
								 responseKeyFormat=ResponseKeyFormat(jsonKeys=JSONSTRING_KEYS, dataFormat=formatdata))
		# if isinstance(res.data, list) and len(res.data) > 0:
		# 	res.data = res.data[0]
		if res.status==ULTIPA.Code.SUCCESS:
			res.data=convertToUser(res)
		return res

	def getSelfInfo(self,
					requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		'''
		Get the current user.

		Args:
			requestConfig: An object of RequestConfig class

		Returns:
			UltipaResponse

		'''
		uqlMaker = UQLMAKER(command=CommandList.getSelfInfo, commonParams=requestConfig)
		res = self.UqlListSimple(uqlMaker=uqlMaker,
								 responseKeyFormat=ResponseKeyFormat(jsonKeys=JSONSTRING_KEYS, dataFormat=formatdata))

		return res

	def createUser(self, request: ULTIPA_REQUEST.CreateUser,
				   requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		'''
		Create a user.

		Args:
			request: An object of CreateUser class

			requestConfig: An object of RequestConfig class

		Returns:
			UltipaResponse

		'''

		uqlMaker = UQLMAKER(command=CommandList.createUser, commonParams=requestConfig)
		params = []
		if request.username:
			params.append(request.username)
		else:
			raise ParameterException(err='username is a required parameter')

		if request.password:
			params.append(request.password)
		else:
			raise ParameterException(err='password is a required parameter')

		if request.graph_privileges:
			params.append(request.graph_privileges)
		else:
			params.append({})

		if request.system_privileges:
			params.append(request.system_privileges)
		else:
			params.append([])

		if request.policies:
			params.append(request.policies)
		else:
			params.append([])	

		if request.property_privileges:
			params.append(request.property_privileges)
		else:
			params.append({})


		uqlMaker.setCommandParams(params)
		return self.uqlSingle(uqlMaker=uqlMaker)

	def dropUser(self, userName:str,
				 requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		'''
		Drop a user.

		Args:
			userName: The name of user

			requestConfig: An object of RequestConfig class

		Returns:
			UltipaResponse

		'''

		uqlMaker = UQLMAKER(command=CommandList.dropUser, commonParams=requestConfig)
		uqlMaker.setCommandParams(userName)
		return self.uqlSingle(uqlMaker=uqlMaker)

	def alterUser(self, request: ULTIPA_REQUEST.AlterUser,
				  requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		'''
		Alter a user.

		Args:
			request: An object of AlterUser class

			requestConfig: An object of RequestConfig class

		Returns:
			UltipaResponse

		'''

		uqlMaker = UQLMAKER(command=CommandList.alterUser, commonParams=requestConfig)
		if request.username:
			uqlMaker.setCommandParams(request.username)
		else:
			raise ParameterException(err='username is a required parameter')

		paramsDict = {}
		if request.password:
			paramsDict.setdefault('password', request.password)

		if request.graph_privileges:
			paramsDict.setdefault('graph_privileges', request.graph_privileges)

		if request.system_privileges:
			paramsDict.setdefault('system_privileges', request.system_privileges)

		if request.policies:
			paramsDict.setdefault('policies', request.policies)

		if request.property_privileges:
			paramsDict.setdefault('property_privileges', request.property_privileges)				

		uqlMaker.addParam('set', paramsDict)
		return self.uqlSingle(uqlMaker=uqlMaker)

	def getUserSetting(self,request:ULTIPA_REQUEST.getUserSetting,
					 requestconfig:RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		
		'''
		Get User Settings .

		Args:
			request: An object of getUserSetting Class

			requestConfig: An object of RequestConfig class

		Returns:
			UltipaResponse

		'''
		
		try:
			request=ultipa_pb2.UserSettingRequest(user_name=request.username,type=request.type,
										 opt=ultipa_pb2.UserSettingRequest.OPTION.OPT_GET)
			clientInfo = self.getClientInfo(graphSetName=requestconfig.graphName, useMaster=requestconfig.useMaster, clientType=ClientType.Leader,
											isGlobal=True,timezone=requestconfig.timeZone, timeZoneOffset=requestconfig.timeZoneOffset)	
			res=clientInfo.Controlsclient.UserSetting(request,metadata=clientInfo.metadata)
			status = FormatType.status(res.status)
			data=res.data
			response = ULTIPA_RESPONSE.Response(status=status,data=data)
			return response
		
		except Exception as e:
			errorRes = ULTIPA_RESPONSE.Response()
			try:
				message = str(e._state.code) + ' : ' + str(e._state.details)
			except:
				message = 'UNKNOWN ERROR'
			errorRes.status = ULTIPA.Status(code=ULTIPA.Code.UNKNOW_ERROR, message=message)	
			return errorRes	
		
	def setUserSetting(self,request:ULTIPA_REQUEST.setUserSetting,
					 requestconfig:RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		
		'''
		set User Settings .

		Args:
			request: An object of setUserSetting Class

			requestConfig: An object of RequestConfig class

		Returns:
			UltipaResponse

		'''
		try:
			request=ultipa_pb2.UserSettingRequest(user_name=request.username,type=request.type,
										 opt=ultipa_pb2.UserSettingRequest.OPTION.OPT_SET,data=request.data)
			clientInfo = self.getClientInfo(graphSetName=requestconfig.graphName, useMaster=requestconfig.useMaster,
								    clientType=ClientType.Leader,isGlobal=True,
									timezone=requestconfig.timeZone, timeZoneOffset=requestconfig.timeZoneOffset)	
			res=clientInfo.Controlsclient.UserSetting(request,metadata=clientInfo.metadata)
			status = FormatType.status(res.status)
			response = ULTIPA_RESPONSE.Response(status=status)
			return response



		except Exception as e:
			errorRes = ULTIPA_RESPONSE.Response()
			try:
				message = str(e._state.code) + ' : ' + str(e._state.details)
			except:
				message = 'UNKNOWN ERROR'
			errorRes.status = ULTIPA.Status(code=ULTIPA.Code.UNKNOW_ERROR, message=message)	
			return errorRes	



			

		

