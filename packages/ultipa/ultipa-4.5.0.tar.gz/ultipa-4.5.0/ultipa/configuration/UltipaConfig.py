# -*- coding: utf-8 -*-
# @Time    : 2023/8/10 18:25
# @Author  : Ultipa
# @Email   : support@ultipa.com
# @File    : UltipaConfig.py
from typing import List
from ultipa.utils.logger import LoggerConfig
from enum import Enum
from ultipa.utils.password2md5 import passwrod2md5


class PasswordEncrypt(Enum):
    MD5 = 1
    LDAP = 2
    NOTHING = 3

class UltipaConfig:
	'''
    Configuration class used to instantiate Ultipa connection.

    This class stores settings for establishing a connection to an Ultipa server. The change of an UltipaConfig object will update the connection it established.
    
    Args:
        - hosts (str): The list of Ultipa server hosts.
        - username (list[str]): The username of server.
        - password (str): The password of server.
		- passwordEncrypt(PasswordEncrypt): Encryption type for password(MD5/LDAP/NOTHING)
        - crtFilePath (str): The file path of SSL certificate when both Ultipa server and client-end are in SSL mode.
        - defaultGraph (str): The name of graphset to use.
        - timeout (int): The timeout for the request in seconds.
        - responseWithRequestInfo (bool): Whether to return request.
        - consistency (bool): Whether to use leader host to guarantee Consistency Read.
        - heartBeat (int): The heartbeat in seconds for all instances, set 0 to turn off heartbeat.
        - maxRecvSize (int): The maximum number of bytes when receiving data.
        - uqlLoggerConfig (LoggerConfig): The object of LoggerConfig class.
        - debug (bool): Whether to use debug mode.
        - timeZone (str): The string of timezone in standard format.
        - timeZoneOffset (any): 1, the number of seconds; 2, a 5-character string such as +0700, -0430.
        
    To enable debug mode, a logger configuration is necessary. If 'debug' is set to True but 'uqlLoggerConfig' is not defined, a LoggerConfig object will be generated for debugging purposes; however, the log will not be written to a file.
	'''

	def __init__(self, hosts:List[str]=None, username:str=None, password:str=None, passwordEncrypt:PasswordEncrypt=PasswordEncrypt.MD5, crtFilePath:str=None, defaultGraph: str = "default",
				 timeout: int = 3600, responseWithRequestInfo: bool = False,
				 consistency: bool = False, heartBeat: int = 10, maxRecvSize: int = -1,
				 uqlLoggerConfig: LoggerConfig = None, debug: bool = False, timeZone=None,
				 timeZoneOffset=None, **kwargs):
		if hosts is None:
			hosts = []
		self.hosts = hosts
		self.username = username
		# self.password = password
		self._password = None
		self.passwordEncrypt=passwordEncrypt
		self.crtFilePath = crtFilePath
		self.defaultGraph = defaultGraph
		self.timeoutWithSeconds = timeout
		self.responseWithRequestInfo = responseWithRequestInfo
		# Read consistency, when set to False, distributes the workload across nodes.
		self.consistency = consistency
		self.uqlLoggerConfig = uqlLoggerConfig
		self.heartBeat = heartBeat
		self.maxRecvSize = maxRecvSize
		self.Debug = debug
		self.timeZone = timeZone
		self.timeZoneOffset = timeZoneOffset
		if kwargs.get("timeoutWithSeconds") is not None:
			self.timeoutWithSeconds = kwargs.get("timeoutWithSeconds")
		
		self.password = password 
	@property
	def password(self):
			return self._password

	@password.setter
	def password(self, value):
			if self.passwordEncrypt == PasswordEncrypt.MD5 and value is not None:
				self._password = passwrod2md5(value)
			else:
				self._password = value			

		# if self.passwordEncrypt==PasswordEncrypt.MD5 and password is not None:
		# 	passworde=passwrod2md5(self.password)
		# 	self.password=passworde
			
	def setDefaultGraphName(self, graph: str):
		self.defaultGraph = graph