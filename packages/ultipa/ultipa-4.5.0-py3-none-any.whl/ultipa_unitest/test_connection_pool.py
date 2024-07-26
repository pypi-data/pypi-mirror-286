from ultipa import UltipaConfig, Connection

from ultipa.connection.connectionPool import UltipaConnectionPool

host =["210.13.32.146:60074"]
defaultConfig = UltipaConfig()
defaultConfig.responseWithRequestInfo = True
defaultConfig.consistency = True
defaultConfig.responseIsMarge = True
# conn = Connection.GetConnection(host,username="root", password="root",defaultConfig=defaultConfig)
# ret = conn.test()
# print(ret)

test = UltipaConnectionPool(host,username="root", password="root",defaultConfig=defaultConfig)
print(test.pool._pool.qsize())
ret = test.get_conn().test()
print(ret)
# print(test.pool._pool.qsize())
# test.destroyConn(test.get_conn())
# print(ret)
# print(test.pool._pool.qsize())

# print(ret)