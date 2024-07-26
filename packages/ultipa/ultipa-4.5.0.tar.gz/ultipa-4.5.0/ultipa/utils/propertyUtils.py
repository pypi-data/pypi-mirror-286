# -*- coding: utf-8 -*-
# @Time    : 2023/1/16 11:06 AM
# @Author  : Ultipa
# @Email   : support@ultipa.com
# @File    : propertyUtils.py
from ultipa.structs.PropertyType import PropertyTypeStr
from ultipa.types import ULTIPA
from typing import List


def isBasePropertyType(type: PropertyTypeStr):
	'''
	Judge whether a data type is a base property type (not a list).

	Args:
		type:

	Returns:

	'''
	if type in [PropertyTypeStr.PROPERTY_STRING,
				PropertyTypeStr.PROPERTY_INT,
				PropertyTypeStr.PROPERTY_INT64,
				PropertyTypeStr.PROPERTY_UINT32,
				PropertyTypeStr.PROPERTY_UINT64,
				PropertyTypeStr.PROPERTY_FLOAT,
				PropertyTypeStr.PROPERTY_DOUBLE,
				PropertyTypeStr.PROPERTY_DATETIME,
				PropertyTypeStr.PROPERTY_TIMESTAMP,
				PropertyTypeStr.PROPERTY_TEXT]:
		return True
	return False


def getPropertyTypesDesc(type: PropertyTypeStr, subTypes: List[PropertyTypeStr]):
	'''
	Generate the format string a list type corresponds to.

	Args:
		type:

		subTypes:

	Returns:
		str[]
	'''
	if type == PropertyTypeStr.PROPERTY_LIST:
		subType = subTypes[0]
		if isBasePropertyType(subType):
			return f"{subType}[]"
	if type == PropertyTypeStr.PROPERTY_SET:
		subType = subTypes[0]
		if isBasePropertyType(subType):
			return f"set({subType})"
	return type
