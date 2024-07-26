from ultipa.utils.logger import LoggerConfig

log = LoggerConfig(name=None,isStream=True)
for i in range(10):
    log.getlogger().info(i)
#
# fs = ''
# lis=['test()','list()']
# fstr = "{}({})".format('key', "'value'")
# print(fstr)
# fstr = fstr.replace('"','')
# lis.append(fstr)
# ret = '.'.join(lis)
# print(ret)