from ultipa.configuration.RequestConfig import RequestConfig
from ultipa.operate.base_extra import BaseExtra
from ultipa.types import ULTIPA_REQUEST, ULTIPA_RESPONSE, ULTIPA
from ultipa.utils import UQLMAKER, CommandList
from ultipa.utils.errors import ParameterException
from ultipa.utils.ResposeFormat import ResponseKeyFormat
from typing import List
from ultipa.structs.Policy import Policy
from ultipa.utils.convert import convertToPolicy
from ultipa.utils.convert import convertToPrivilege


JSONSTRING_KEYS = ["graphPrivileges", "systemPrivileges", "policies", "policy", "privilege"]
formatdata = ['graph_privileges']


class PolicyExtra(BaseExtra):

	'''
		Processing class that defines settings for policy related operations.
	'''

	def showPolicy(self,
				   requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.ResponseListPolicy:
		'''
		Show policy list.

		Args:
			requestConfig: An object of RequestConfig class

		Returns:
			ResponsePolicy

		'''
		uqlMaker = UQLMAKER(command=CommandList.showPolicy, commonParams=requestConfig)
		res = self.UqlListSimple(uqlMaker=uqlMaker,
								 responseKeyFormat=ResponseKeyFormat(jsonKeys=JSONSTRING_KEYS, dataFormat=formatdata))
		if len(res.data)>0:
			res.data=convertToPolicy(res)
		return res

	def showPrivilege(self,
					  requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.ResponsePrivilege:
		'''
		Show privilege list.

		Args:
			requestConfig: An object of RequestConfig class

		Returns:
			ResponsePrivilege

		'''

		uqlMaker = UQLMAKER(command=CommandList.showPrivilege, commonParams=requestConfig)
		res = self.UqlListSimple(uqlMaker=uqlMaker,
								 responseKeyFormat=ResponseKeyFormat(jsonKeys=JSONSTRING_KEYS))
		if len(res.data)>0:
			res.data=convertToPrivilege(res)
		return res

	def getPolicy(self, policyName:str,
				  requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.ResponsePolicy:
		'''
		Get a policy.

		Args:
			name: The name of policy

			requestConfig: An object of RequestConfig class

		Returns:
			ResponsePolicy

		'''

		uqlMaker = UQLMAKER(command=CommandList.getPolicy, commonParams=requestConfig)
		uqlMaker.setCommandParams(policyName)
		res = self.UqlListSimple(uqlMaker=uqlMaker,
								 responseKeyFormat=ResponseKeyFormat(jsonKeys=JSONSTRING_KEYS, dataFormat=formatdata))
		# if isinstance(res.data, list) and len(res.data) > 0:
		# 	res.data = res.data[0]
		if res.status.code==ULTIPA.Code.SUCCESS:
			res.data=convertToPolicy(res)
		return res

	def createPolicy(self, policy: Policy,
					 requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		'''
		Create a policy.

		Args:
			request:  An object of Policy class

			requestConfig: An object of RequestConfig class

		Returns:
			UltipaResponse

		'''

		uqlMaker = UQLMAKER(command=CommandList.createPolicy, commonParams=requestConfig)
		paramsP = [policy.name]
		if policy.graphPrivileges:
			paramsP.append(policy.graphPrivileges)
		else:
			paramsP.append({})

		if policy.systemPrivileges:
			paramsP.append(policy.systemPrivileges)
		else:
			paramsP.append([])

		if policy.policies:
			paramsP.append(policy.policies)	
		else:
			paramsP.append([])

		if policy.propertyPrivileges:
			paramsP.append(policy.propertyPrivileges)
		else:
			paramsP.append({})	

		uqlMaker.setCommandParams(paramsP)
		res = self.uqlSingle(uqlMaker=uqlMaker)
		return res

	def alterPolicy(self, policy: Policy,
					requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		'''
		Alter a policy.

		Args:
			request:  An object of Policy class

			requestConfig: An object of RequestConfig class

		Returns:
			UltipaResponse

		'''

		uqlMaker = UQLMAKER(command=CommandList.alterPolicy, commonParams=requestConfig)
		uqlMaker.setCommandParams(policy.name)
		params = {}
		if policy.systemPrivileges is not None:
			params.update({"system_privileges": policy.systemPrivileges})
		if policy.graphPrivileges is not None:
			params.update({"graph_privileges": policy.graphPrivileges})

		if policy.policies is not None:
			params.update({"policies": policy.policies})	

		if policy.propertyPrivileges is not None:
			params.update({"property_privileges": policy.propertyPrivileges})

			
		uqlMaker.addParam('set', params, notQuotes=True)
		res = self.uqlSingle(uqlMaker=uqlMaker)
		return res

	def dropPolicy(self, policyName:str,
				   requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		'''
		Drop a policy.

		Args:
			policyName:  Name of policy to be dropped
			requestConfig: An object of RequestConfig class

		Returns:
			UltipaResponse

		'''

		uqlMaker = UQLMAKER(command=CommandList.dropPolicy, commonParams=requestConfig)
		uqlMaker.setCommandParams(policyName)
		res = self.uqlSingle(uqlMaker=uqlMaker)
		return res

	def grantPolicy(self, username: str = '', graphPrivileges: dict = None,
				 systemPrivileges: List[str] = None, policies: List[str] = None, propertyPrivileges:dict=None,
					requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		'''
		Grant privileges and policies to a user.

		Args:
			username (str): The username to grant privileges and policies.

        	graphPrivileges (dict): Dictionary containing graph privileges.

        	systemPrivileges (List[str]): List of system privileges.

        	policies (List[str]): List of policies to grant.
			
			propertyPrivileges(dict): Dictionary containing property privileges

        	requestConfig (RequestConfig): An object of RequestConfig class

		Returns:
			UltipaResponse

		'''

		uqlMaker = UQLMAKER(command=CommandList.grantUser, commonParams=requestConfig)
		if username:
			uqlMaker.setCommandParams(username)
		else:
			raise ParameterException(err='username is a required parameter')

		paramsDict = {}
		if graphPrivileges:
			paramsDict.setdefault('graph_privileges', graphPrivileges)

		if systemPrivileges:
			paramsDict.setdefault('system_privileges',systemPrivileges)

		if policies:
			paramsDict.setdefault('policies',policies)	
		
		if propertyPrivileges:
			paramsDict.setdefault('property_privileges',propertyPrivileges)	


		uqlMaker.addParam('params', paramsDict, notQuotes=True)
		res = self.uqlSingle(uqlMaker=uqlMaker)
		return res

	def revokePolicy(self, username: str = '', graphPrivileges: dict = None,
				 systemPrivileges: List[str] = None, policies: List[str] = None, propertyPrivileges:dict=None,
					 requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		'''
		Revoke privileges and policies from a user.

		Args:
			username (str): The username to revoke privileges and policies.

        	graphPrivileges (dict): Dictionary containing graph privileges.

        	systemPrivileges (List[str]): List of system privileges.

			propertyPrivileges(dict): Dictionary containing property privileges

        	policies (List[str]): List of policies to revoke.

        	requestConfig (RequestConfig): An object of RequestConfig class

		Returns:
			UltipaResponse

		'''

		uqlMaker = UQLMAKER(command=CommandList.revoke, commonParams=requestConfig)
		if username:
			uqlMaker.setCommandParams(username)
		else:
			raise ParameterException(err='username is a required parameter')

		paramsDict = {}
		if graphPrivileges:
			paramsDict.setdefault('graph_privileges', graphPrivileges)

		if systemPrivileges:
			paramsDict.setdefault('system_privileges', systemPrivileges)

		if propertyPrivileges:
			paramsDict.setdefault('property_privileges',propertyPrivileges)	

		if policies:
			paramsDict.setdefault('policies', policies)	
		uqlMaker.addParam('params', paramsDict, notQuotes=True)
		res = self.uqlSingle(uqlMaker=uqlMaker)
		return res
