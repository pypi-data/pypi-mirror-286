# from functools import singledispatch
#
# @singledispatch
# def fun(arg, verbose=True):
#     if verbose:
#         print("Let me just say,", end=" ")
#         print(arg)
#
#
# from functools import singledispatch
#
#
# @singledispatch
# def add(obj):
#     return obj
#
#
# @add.register(int)
# def _(add):
#     print("int类型")
#
#
# @add.register(str)
# def _(add):
#     print("str类型")
#
#
# @add.register(list)
# def _(add):
#     print("list类型")
#     return 123
#
#
# @add.register(tuple)
# def _(add):
#     print("tuple类型")
#
#
# @add.register(dict)
# def _(add):
#     print("dict类型")
#
#
# @add.register(set)
# def _(add):
#     print(add)
#     print("set类型")
#

# add([1, 2, 3])
# import time
# from datetime import datetime, date
#
#
# class OwenTime:
#
#     def __init__(self,year = 0,month = 0,day = 0,hour = 0,minute = 0,second = 0,microsecond = 0):
#         self.year = year
#         self.month = month
#         self.day = day
#         self.hour = hour
#         self.minute = minute
#         self.second = second
#         self.microsecond = microsecond

    # def getTimeStemp(self):
from past.builtins import raw_input

DIR_path_BFG = '/Users/qinshiju/Documents/private-workespace/BFG'
DIR_path_cmb = '/Users/qinshiju/Documents/Ultipa/cmb-debt-assets-frontend'
DIR_PROJECT = DIR_path_cmb
todo = raw_input(f'''请选择项目路径，输入数字即可
1 :{DIR_path_cmb}
2 :{DIR_path_BFG}
其他数字自动退出
请输入：''')
if todo == "1":
 DIR_PROJECT = DIR_path_cmb
if todo == "2":
 DIR_PROJECT = DIR_path_BFG

# if __name__ == '__main__':
    # ret = add(set())
    # print(ret)
    # dt = DateTimestamp()  # 返回当前时间
    # dt = DateTimestamp("2020-03-20 10:00:00")  # 返回指定datetime的
    # dt = DateTimestamp(0)
    # print(dt.datetime)
