# -*- coding: utf-8 -*-
# @Time    : 2022/6/23 1:21 下午
# @Author  : Ultipa
# @Email   : support@ultipa.com
# @File    : test_write.py
import time
import unittest
import csv


def wrapper(func):
    def inner(*args, **kwargs):
        start_time = time.time()
        res = func(*args, **kwargs)
        end_time = time.time()
        result = end_time - start_time
        print('func time is %.3fs' % result)
        return res
    return inner

class TestUltipaMethods(unittest.TestCase):

	@wrapper
	def test_write(self):
		with open("./test.csv","w") as f:
			writer = csv.writer(f)
			for i in range(200000):
				writer.writerow([ f"{i}_1",f"v{i}_2",f"v{i}_3"])
				# data = f"{i}_1,v{i}_2,v{i}_3 \n"
				# f.write(data)
				if i == 100000:
					f.flush()



	@wrapper
	def test_read(self):
		with open("./test.csv","r") as f:
			reader = csv.reader(f)
			for i,j in enumerate(reader):
				if i%100000 == 0:
					print(i)



