# -*- coding: utf-8 -*-
# @Time    : 2023/8/4 18:14
# @Author  : Ultipa
# @Email   : support@ultipa.com
# @File    : InsertConfig.py
from ultipa.configuration.RequestConfig import RequestConfig
from ultipa.structs.InsertType import InsertType
from ultipa.structs.Retry import Retry


class InsertConfig(RequestConfig):
	'''
    Configuration class for the interface of insert operation.

    This class provides settings for inserting metadata.
    
    Args:
        - insertType (InsertType): The mode of insert request (NORMAL/UPSERT/OVERWRITE).
        - graphName (str): The name of graphset to use.
        - timeout (int): The timeout for the request in seconds.
        - retry (Retry): The object of Retry configuration classwhen the request fails
        - stream (bool): Whether to return stream
        - useHost (str): The designated host the request will be sent to, or sent to a random host if not set
        - useMaster (bool):	Whether to send the request to the leader to guarantee Consistency Read
        - CreateNodeIfNotExist (bool): Whether to create start/end nodes of edge when these nodes do not exist in the graphset
        - timeZone (str): The string of timezone in standard format
        - timeZoneOffset (any): 1, the number of seconds; 2, a 5-character string such as +0700, -0430
	'''
	def __init__(self, insertType: InsertType, graphName: str = '', timeout: int = 3600,
				 retry: Retry = Retry(), stream: bool = False, useHost: str = None, useMaster: bool = False,
				 CreateNodeIfNotExist: bool = False, timeZone=None, timeZoneOffset=None, **kwargs):
		super().__init__(graphName, timeout, retry, stream, useHost, useMaster, timeZone=timeZone,
						 timeZoneOffset=timeZoneOffset)
		self.insertType = insertType
		if kwargs.get("silent") is not None:
			self.silent = kwargs.get("silent")
		else:
			self.silent = True
		if kwargs.get("batch") is not None:
			self.batch = kwargs.get("batch")
		if kwargs.get("n") is not None:
			self.n = kwargs.get("n")
		if kwargs.get("timeoutWithSeconds") is not None:
			self.timeoutWithSeconds = kwargs.get("timeoutWithSeconds")
		self.createNodeIfNotExist = CreateNodeIfNotExist
