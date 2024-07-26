# -*- coding: utf-8 -*-
# @Time    : 2023/4/4 16:53
# @Author  : Ultipa
# @Email   : support@ultipa.com
# @File    : test_backup.py
import unittest
from datetime import date

import pytest

from ultipa import Connection, ULTIPA_REQUEST, ULTIPA, FILTER, InsertConfig, InsertNode
from ultipa.connection.connection_base import ClientType
from ultipa.utils import UQLMAKER
from ultipa.utils.ufilter.new_ufilter import FilterEnum
from ultipa_unitest import conn


class TestUltipaMethods(unittest.TestCase):
	gname = 'default'

	def test(self):
		ret = conn.test()
		print(ret)
	def test_backup(self):

		ret = conn.backupData("/opt/ultipa-server/exportData/backup")
		print(ret.toJSON())