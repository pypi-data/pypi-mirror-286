from ultipa.configuration.RequestConfig import RequestConfig
from ultipa.operate.base_extra import BaseExtra
from ultipa.types import ULTIPA_REQUEST, ULTIPA, ULTIPA_RESPONSE
from ultipa.utils import UQLMAKER, CommandList
import json
from typing import Union,Optional
from ultipa.utils.convert import convertToAnyObject
from ultipa.utils.ResposeFormat import ResponseKeyFormat
from ultipa.types.types_request import TaskStatus
from ultipa.utils.convert import convertToTop


class ALGO_RETURN_TYPE:
	ALGO_RETURN_REALTIME = 1
	ALGO_RETURN_WRITE_BACK = 2
	ALGO_RETURN_VISUALIZATION = 4


class TaskExtra(BaseExtra):
	'''
	Processing class that defines settings for task and process related operations.
	'''

	def top(self,
			requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.ResponseListTop:
		'''
		Top real-time processes.

		Args:
			requestConfig: An object of RequestConfig class

		Returns:
			ResponseListTop

		'''
		uqlMaker = UQLMAKER(command=CommandList.top, commonParams=requestConfig)
		res = self.UqlListSimple(uqlMaker)
		if len(res.data)>0:
			res.data=convertToTop(res)
		return res

	def kill(self, processId: str = None, all: bool = False,
			 requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.Response:
		'''
		Kill real-time processes.

		Args:
			id: The ID of real-time process

			all: Whether to kill all real-time processes

			requestConfig: An object of RequestConfig class

		Returns:
			Response

		'''
		commonP = []
		if processId:
			commonP = processId
		if all:
			commonP = '*'
		uqlMaker = UQLMAKER(command=CommandList.kill, commonParams=requestConfig)
		uqlMaker.setCommandParams(commonP)
		res = self.uqlSingle(uqlMaker)
		return res

	def showTask(self, algoNameOrId: Optional[Union[int, str]] = None, status: TaskStatus=None,
				 config: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.ResponseListTask:
		'''
		Show back-end tasks.

		Args:

        	algoNameOrld (str): The name of the task algo to show

        	status (str): The status of the tasks to retrieve.

        	config (RequestConfig): An object of RequestConfig class.

		Returns:
			ResponseListTask

		'''

		_jsonKeys = ['taskJson']
		uqlMaker = UQLMAKER(command=CommandList.showTask, commonParams=config)
		commonP = []

		# if all:
		# 	commonP.append('*')

		# else:	

		if isinstance(algoNameOrId, str) or algoNameOrId is None:
			if algoNameOrId and status:
					commonP.append(algoNameOrId)
					commonP.append(status.value)
			if algoNameOrId and not status:
					commonP.append(algoNameOrId)
					commonP.append('*')
			if not algoNameOrId and status:
					commonP.append('*')
					commonP.append(status.value)
		
		elif isinstance(algoNameOrId, int):
				commonP=algoNameOrId

		uqlMaker.setCommandParams(commandP=commonP)
		res = self.UqlListSimple(uqlMaker=uqlMaker, responseKeyFormat=ResponseKeyFormat(jsonKeys=_jsonKeys))
		newDatas = []
		if res.data:
			for obj in res.data:
				obj = obj.__dict__
				newData = ULTIPA_RESPONSE.Task()
				taskJson = obj.get("taskJson", {})
				newData.param = json.loads(taskJson.get("param", "{}"))
				newData.result = taskJson.get("result")
				task_info = taskJson.get("task_info", {})

				if task_info.get('status_code'):
					task_info["status_code"] = ULTIPA.TaskStatusString[task_info.get("TASK_STATUS")]
				if task_info.get('engine_cost'):
					task_info["engine_cost"] = task_info.get("writing_start_time", 0) - task_info.get("start_time", 0)

				newData.task_info = convertToAnyObject(task_info)
				return_type_get = int(task_info.get('return_type', 0))
				return_type = ULTIPA_RESPONSE.Return_Type()
				return_type.is_realtime = True if return_type_get & ALGO_RETURN_TYPE.ALGO_RETURN_REALTIME else False
				return_type.is_visualization = True if return_type_get & ALGO_RETURN_TYPE.ALGO_RETURN_VISUALIZATION else False
				return_type.is_wirte_back = True if return_type_get & ALGO_RETURN_TYPE.ALGO_RETURN_WRITE_BACK else False
				newData.task_info.__setattr__('return_type', return_type)
				newDatas.append(newData)
			res.data = newDatas
		return res

	def clearTask(self, algoNameOrId: Optional[Union[int, str]] = None, status:TaskStatus=None,
				  config: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.Response:
		'''
		Clear back-end tasks.

		Args:

        	algoNameOrId (str): The name of the algotask to clear.

        	status (str): The status of the tasks to clear.

        	requestConfig (RequestConfig): An object of RequestConfig class.

		Returns:
			Response

		'''

		uqlMaker = UQLMAKER(command=CommandList.clearTask, commonParams=config)
		commonP = []
		# if all:
		# 	commonP.append('*')
		# else:


		if isinstance(algoNameOrId, str) or algoNameOrId is None:
			if algoNameOrId and status:
					commonP.append(algoNameOrId)
					commonP.append(status.value)
			if algoNameOrId and not status:
					commonP.append(algoNameOrId)
					commonP.append('*')
			if not algoNameOrId and status:
					commonP.append('*')
					commonP.append(status.value)
		
		elif isinstance(algoNameOrId, int):
				commonP = algoNameOrId
		# if id:
		# 		commonP = id

		uqlMaker.setCommandParams(commandP=commonP)
		res = self.UqlUpdateSimple(uqlMaker)

		return res

	def stopTask(self, id: str = None,
				 config: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.Response:
		'''
		Stop back-end tasks.

		Args:
			id: The ID of back-end task

			all: Whether to stop all back-end tasks that are computing

			requestConfig: An object of RequestConfig class

		Returns:
			Response

		'''
		uqlMaker = UQLMAKER(command=CommandList.stopTask, commonParams=config)
		commonP = []
		# if all:
		# 	commonP = '*'
		# if id:
		commonP = id
		uqlMaker.setCommandParams(commandP=commonP)
		return self.UqlUpdateSimple(uqlMaker)
	

	def pauseTask(self, id: int = None, all: bool = False,
				 requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.ResponseCommon:
		'''
		Stop back-end tasks.

		Args:
			id: The ID of back-end task

			all: Whether to pause all back-end tasks that are computing

			requestConfig: An object of RequestConfig class

		Returns:
			ResponseCommon

		'''
		uqlMaker = UQLMAKER(command=CommandList.pauseTask, commonParams=requestConfig)
		commonP = []
		if all:
			commonP = '*'
		if id:
			commonP = id
		uqlMaker.setCommandParams(commandP=commonP)
		return self.UqlUpdateSimple(uqlMaker)
	
	def resumeTask(self, id: int = None, all: bool = False,
				 requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.ResponseCommon:
		'''
		Stop back-end tasks.

		Args:
			id: The ID of back-end task

			all: Whether to resume all back-end tasks

			requestConfig: An object of RequestConfig class

		Returns:
			ResponseCommon

		'''
		uqlMaker = UQLMAKER(command=CommandList.resumeTask, commonParams=requestConfig)
		commonP = []
		if all:
			commonP = '*'
		if id:
			commonP = id
		uqlMaker.setCommandParams(commandP=commonP)
		return self.UqlUpdateSimple(uqlMaker)
	


	def clusterInfo(self,
					requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.ClusterInfo:
		'''
		Show cluster information.

		Args:
			requestConfig: An object of RequestConfig class

		Returns:
			ClusterInfo

		'''
		self.refreshRaftLeader(redirectHost='', requestConfig=requestConfig)
		result = []
		if not requestConfig.graphName:
			graphSetName = 'default'
		else:
			graphSetName = requestConfig.graphName
		for peer in self.hostManagerControl.getAllHostStatusInfo(graphSetName):
			info = ULTIPA_RESPONSE.Cluster()
			info.status = peer.status
			info.host = peer.host
			info.isLeader = peer.isLeader
			info.isFollowerReadable = peer.isFollowerReadable
			info.isAlgoExecutable = peer.isAlgoExecutable
			info.isUnset = peer.isUnset
			info.cpuUsage = None
			info.memUsage = None
			if peer.status:
				ret = self.stats(requestConfig=RequestConfig(host=peer.host))
				if ret.status.code == ULTIPA.Code.SUCCESS:
					info.cpuUsage = ret.data.cpuUsage
					info.memUsage = ret.data.memUsage

			result.append(info)
		res = ULTIPA_RESPONSE.Response()
		res.data = result
		return res
