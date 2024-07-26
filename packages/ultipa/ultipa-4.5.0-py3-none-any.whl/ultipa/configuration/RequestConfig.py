# -*- coding: utf-8 -*-
# @Time    : 2023/8/1 10:46
# @Author  : Ultipa
# @Email   : support@ultipa.com
# @File    : requestConfig.py
from ultipa.structs.Retry import Retry


class RequestConfig:
	'''
    Configuration class for the interface of any non-insert operation.

    This class provides settings for all the operations other than inserting metadata.
    
    Args:
        - graphName (str): The name of graphset to use.
        - timeout (int): The timeout for the request in seconds.
        - retry (Retry): The object of Retry configuration class when the request fails
        - stream (bool): Whether to return stream
        - host (str): The designated host the request will be sent to, or sent to a random host if not set
        - useMaster (bool):	Whether to send the request to the leader to guarantee Consistency Read
        - threadNum (int): The number of threads used for the request
        - timeZone (str): The string of timezone in standard format
        - timeZoneOffset (any): 1, the number of seconds; 2, a 5-character string such as +0700, -0430
	'''

	def __init__(self, graphName: str = '', timeout: int = 3600, retry: Retry = Retry(),
				 stream: bool = False, host: str = None, useMaster: bool = False, threadNum: int = None,
				 timeZone: str = None, timeZoneOffset: any = None):
		self.graphName = graphName
		self.timeoutWithSeconds = timeout
		self.retry = retry
		self.stream = stream
		self.useHost = host
		self.useMaster = useMaster
		self.threadNum = threadNum
		self.timeZone = timeZone
		self.timeZoneOffset = timeZoneOffset

