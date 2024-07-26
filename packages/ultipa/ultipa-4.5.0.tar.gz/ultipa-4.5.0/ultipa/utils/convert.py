import json
from typing import List

from ultipa.structs.BaseModel import BaseModel
# from ultipa.types.types_response import UltipaResponse
from ultipa.structs.DBType import DBType
from ultipa.structs.Index import Index
from ultipa.structs.User import User
from ultipa.structs.Policy import Policy
from ultipa.structs.Privilege import Privilege
from ultipa.structs.GraphSet import GraphSet
from ultipa.structs.Stats import Stats
from ultipa.structs.Top import Top
from ultipa.structs.Algo import Algo

class Any(BaseModel):
	'''
	Any model
	'''
	def __str__(self):
		return str(self.__dict__)

	pass


def convertToAnyObject(dict1: dict):
	'''
	Convert Dict to Object.

	Args:
		dict1:

	Returns:

	'''
	obj = Any()
	for k in dict1.keys():
		v = dict1[k]
		if isinstance(v, list):
			for i, n in enumerate(v):
				if isinstance(n, dict):
					v[i] = convertToAnyObject(n)
		# if isinstance(v, dict):
		#     v = convertToAnyObject(v)
		obj.__setattr__(k, v)
	return obj


def convertToListAnyObject(list1: List[dict]):
	'''
	Convert List[Dict] to Object.

	Args:
		list1:

	Returns:

	'''
	if not list1 and isinstance(list1, list):
		return list1
	if not list1:
		return
	newList = []
	for dict1 in list1:
		newList.append(convertToAnyObject(dict1))
	return newList


def convertTableToDict(table_rows, headers):
	'''
	Convert Table to Object.

	Args:
		table_rows:
		headers:

	Returns:

	'''
	newList = []
	for data in table_rows:
		dic = {}
		for index, header in enumerate(headers):
			dic.update({header.get("property_name"): data[index]})
		newList.append(dic)
	return newList

def convertToGraph(res):
	if isinstance(res.data, list) and len(res.data) > 1:
		graphdata=res.data
		graphlist=[]
		for graph in graphdata:
			graphlist.append(GraphSet(
						id=graph.id,
						name=graph.name,
						totalNodes=graph.totalNodes,
						totalEdges=graph.totalEdges,
						description=graph.description,
						status=graph.status
			))

		return graphlist	
	else:
		graph=res.data[0]
		return GraphSet(
						id=graph.id,
						name=graph.name,
						totalNodes=graph.totalNodes,
						totalEdges=graph.totalEdges,
						description=graph.description,
						status=graph.status
			)


def convertToIndex( res,all:bool=True, dbtype:DBType=None):
	nodeindex=[]
	edgeindex=[]
	indexdata=[]
	if all:
		nodeindex=res.data[0].data	
		edgeindex=res.data[1].data
	elif dbtype==DBType.DBNODE:
		nodeindex=res.data[0].data
	elif dbtype==DBType.DBEDGE:	
		edgeindex=res.data[0].data

	if nodeindex:
			for index in nodeindex:
				indexdata.append(Index(
					name=index.name,
					properties=index.properties,
					schema=index.schema,
					size=index.size,
					status=index.status,
					dbType=DBType.DBNODE
				))
	if edgeindex:
			for index in edgeindex:
				indexdata.append(Index(
					name=index.name,
					properties=index.properties,
					schema=index.schema,
					size=index.size,
					status=index.status,
					dbType=DBType.DBEDGE
				))		
	return indexdata


def convertToFullText( res,all:bool=True, dbtype:DBType=None):
	nodeindex=[]
	edgeindex=[]
	indexdata=[]
	if all:
		nodeindex=res.data[0].data	
		edgeindex=res.data[1].data
	elif dbtype==DBType.DBNODE:
		nodeindex=res.data[0].data
	elif dbtype==DBType.DBEDGE:	
		edgeindex=res.data[0].data

	if nodeindex:
			for index in nodeindex:
				indexdata.append(Index(
					name=index.name,
					properties=index.properties,
					schema=index.schema,
					status=index.status,
					dbType=DBType.DBNODE
				))
	if edgeindex:
			for index in edgeindex:
				indexdata.append(Index(
					name=index.name,
					properties=index.properties,
					schema=index.schema,
					status=index.status,
					dbType=DBType.DBEDGE
				))		
	return indexdata

def convertToUser(res):
	if isinstance(res.data, list) and len(res.data) > 1:
		userdata=res.data
		datalist=[]
		for data in userdata:
			datalist.append(User(
				username=data.username,
				systemPrivileges=data.systemPrivileges,
				graphPrivileges=data.graphPrivileges,
				create=data.create,
				propertyPrivileges=data.propertyPrivileges,
				policies=data.policies
			))

		return datalist	
	else:
		data=res.data[0]
		return User(
				username=data.username,
				systemPrivileges=data.systemPrivileges,
				graphPrivileges=data.graphPrivileges,
				create=data.create,
				propertyPrivileges=data.propertyPrivileges,
				policies=data.policies
			)
		
def convertToPolicy(res):
	if isinstance(res.data, list) and len(res.data) > 1:
		policydata=res.data
		policylist=[]
		for data in policydata:
			policylist.append(Policy(
				name=data.name,
				systemPrivileges=data.systemPrivileges,
				graphPrivileges=data.graphPrivileges,
				policies=data.policies,
				propertyPrivileges=data.propertyPrivileges
			))

		return policylist	
	else:
		data=res.data[0]
		return Policy(
				name=data.name,
				systemPrivileges=data.systemPrivileges,
				graphPrivileges=data.graphPrivileges,
				policies=data.policies,
				propertyPrivileges=data.propertyPrivileges
			)
	
def convertToPrivilege(res):
	if isinstance(res.data, list) and len(res.data) > 1:
		privilegedata=res.data
		privilegelist=[]
		for data in privilegedata:
			privilegelist.append(Privilege(
				systemPrivileges=data.systemPrivileges,
				graphPrivileges=data.graphPrivileges
			))

		return privilegelist	
	else:
		data=res.data[0]
		return Privilege(
				systemPrivileges=data.systemPrivileges,
				graphPrivileges=data.graphPrivileges
			)	
	

def convertToStats(res):
	statsdata=res.data[0]
	server_type = getattr(statsdata, 'serverType', None) or getattr(statsdata, 'severType', None)
	return Stats(
		cpuUsage=statsdata.cpuUsage,
		memUsage=statsdata.memUsage,
		company=statsdata.company,
		cpuCores=statsdata.cpuCores,
		expiredDate=statsdata.expiredDate,
		serverType=server_type,
		version=statsdata.version
	)	

def convertToTop(res):
	if isinstance(res.data, list) and len(res.data) > 0:
		topdata=res.data
		toplist=[]
		for data in topdata:
			toplist.append(Top(
			process_id=data.process_id,
			process_uql=data.process_uql,
			duration=data.duration,
			status=data.status
			))

	return toplist


def convertToAlgo(res):
	if isinstance(res.data, list) and len(res.data) > 0:
		algodata=res.data
		algolist=[]
		for data in algodata:
			algolist.append(Algo(
				name=data.name,
				description=data.param['description'],
				version=data.param['version'],
				result_opt=data.param['result_opt'],
				parameters=data.param['parameters'],
            write_to_stats_parameters=data.param.get('write_to_stats_parameters', None),
            write_to_db_parameters=data.param.get('write_to_db_parameters', None),
            write_to_file_parameters=data.param.get('write_to_file_parameters', None)
			# write_to_client_normal_parameters=data.param.get('write_to_client_normal_parameters', None),
			# write_to_client_stream_parameters=data.param.get('write_to_client_stream_parameters', None)
			))

	return algolist		
		







