# -*- coding: utf-8 -*-
# @Time    : 2023/4/4 09:44
# @Author  : Ultipa
# @Email   : support@ultipa.com
# @File    : test_ultipa_datetime.py
import time

from ultipa.utils.ultipa_datetime import UltipaDatetime

if __name__ == '__main__':
	data_str = '2021-03-09 14:46:50'
	# print(pytz.all_timezones)
	# timestamp = 1649056800
	# timestamp = UltipaDatetime.timestampStr2timestampInt(data_str)
	#
	# utc_dt = datetime.datetime.utcfromtimestamp(timestamp).replace(tzinfo=pytz.utc)
	# new_timezone = pytz.timezone('US/Aleutian')
	# shanghai_dt = utc_dt.astimezone(new_timezone)
	# print(timestamp)
	# print(shanghai_dt.isoformat())

	# data = datetime.datetime.strptime(str_date, "%Y-%m-%d %H:%M:%S.%f")
	# print(data)
	# data = datetime.datetime.strptime(str_date, "%Y-%m-%d %H:%M:%S")
	# print(data)

	# ret = datetime.datetime.strptime(str, "%Y-%m-%d %H:%M:%S.%f")
	# print("str",ret)

	# ret = datetime.datetime.now()
	# print(ret)
	# ret1= UltipaDatetime().datetimeStr2datetimeInt(ret)
	# print(ret1)
	# ret= UltipaDatetime().datetimeInt2datetimeStr(ret1)
	# print(ret)
	# print(pytz.all_timezones)
	# ret = pytz.timezone("Asia/Shanghai")

	# ret = UltipaDatetime().timestampInt2timestampStr(0)
	ret = UltipaDatetime().timestampStr2timestampInt(data_str)
	print(ret)
	print(time.time())
	print(UltipaDatetime().timestampInt2timestampStr(ret))

	# ret = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
	# print(type(ret))

	# 解析带有时区信息的时间字符串
	# time_str = '2022-04-05T12:34:56+08:00'
	# # time_str = '2022-04-05T12:34:56+00:00'
	# dt = parse(time_str)
	# print(int(dt.utcoffset().total_seconds() / 3600))

	# local_tz = pytz.timezone('local')
	# tz = pytz.timezone(local_tz.zone)
	# print(tz)
	#
	# local_tz = tzlocal.get_localzone().zone
	# print(local_tz)
	# tz = pytz.timezone(local_tz)
	# offset_hours = int(tz._utcoffset.total_seconds() / 3600)
	# print(offset_hours)
