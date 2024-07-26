# -*- coding: utf-8 -*-
# @Time    : 2022/1/12 11:24 上午
# @Author  : Ultipa
# @Email   : support@ultipa.com
# @File    : test_keepAlive.py
import time
import unittest

from ultipa import ULTIPA_REQUEST, ULTIPA
from ultipa_unitest import conn


class TestUltipaMethods(unittest.TestCase):

    def test_uql_find_edges(self):
        # conn.defaultConfig.uqlLoggerConfig=LoggerConfig(logger=getlogger(name='test',filename='test.log',IsWriteToFile=True),isDetailed=False)
        ret = conn.uql("find().nodes() return nodes{*} limit 10")
        print(ret.toJSON())
        conn.keepConnectionAlive(2)
        ret = conn.uql("find().nodes() return nodes{*} limit 10")
        print(ret.toJSON())
        time.sleep(10.1)
        # conn.removeConnectionAlive()
        ret = conn.uql("find().nodes() return nodes{*} limit 10")
        print(ret.toJSON())
        conn.stopConnectionAlive()
        time.sleep(5)
        # conn.removeConnectionAlive()

    def test_uql_find_edges1(self):
        # conn.defaultConfig.uqlLoggerConfig=LoggerConfig(logger=getlogger(name='test',filename='test.log',IsWriteToFile=True),isDetailed=False)

        ret = conn.uql("find().nodes() return nodes{*} limit 10")
        print(ret.toJSON())
        # time.sleep(10.1)
        # ret = conn.uql("find().nodes() return nodes{*} limit 10")
        # print(ret.toJSON())
        time.sleep(12)

    def test_time(self):
        import threading
        import time
        def fun_timer():
            print('Hello Timer!')
            print(time.time())

        while True:
            timer = threading.Timer(5, fun_timer)  # 等待5s钟调用一次fun_timer() 函数
            timer.start()
            timer.join()

    # def test_loop(self):
    #     import time
    #     from timeloop import Timeloop
    #     from datetime import timedelta
    #     tl = Timeloop()
    #
    #     @tl.job(interval=timedelta(seconds=2))
    #     def sample_job_every_2s():
    #         print("2s job current time : {}".format(time.ctime()))
    #
    #     # @tl.job(interval=timedelta(seconds=5))
    #     # def sample_job_every_5s():
    #     #     print("5s job current time : {}".format(time.ctime()))
    #     #
    #     # @tl.job(interval=timedelta(seconds=10))
    #     # def sample_job_every_10s():
    #     #     print("10s job current time : {}".format(time.ctime()))
    def test_sh(self):
        import datetime
        import time
        import sched
        def time_printer():
            now = datetime.datetime.now()
            ts = now.strftime('%Y-%m-%d %H:%M:%S')
            print('do func time :', ts)
            loop_monitor()

        def loop_monitor():
            s = sched.scheduler(time.time, time.sleep)  # 生成调度器
            s.enter(5, 1, time_printer, ())
            s.run()

        loop_monitor()


    def test_async(self):

        import asyncio

        async def function_asyc():
            i = 0

            while True:
                i += 1
                if i % 50000 == 0:
                    print("Hello, I'm Abhishek")
                    print("GFG is Great")
                    await asyncio.sleep(1)

        async def function_2():
            while True:
                await asyncio.sleep(3)
                print("\n HELLO WORLD \n")

        loop = asyncio.get_event_loop()
        # asyncio.ensure_future(function_asyc())
        asyncio.run(function_2())
        print("\n HELLO \n")






