import datetime
import unittest

from ultipa.utils.ultipa_datetime import UltipaDatetime


class TestDatetime(unittest.TestCase):

	def test_datetime(self):
		# ret = datetime.datetime(2022, 8, 12, 22, 11, 22)
		ret = datetime.datetime.now()
		if isinstance(ret,datetime.datetime):
			# print(type(ret))
			# print(str(ret))
			UltipaDatetime.datetimeStr2datetimeInt(ret)

