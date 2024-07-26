from ultipa import UltipaConfig
import threading

from multiprocessing.dummy import Pool as MPThreadPool #线程池

from ultipa.connection.connectionPool import UltipaConnectionPool

host =["192.168.1.85:40101"]
defaultConfig = UltipaConfig()
defaultConfig.responseWithRequestInfo = True
defaultConfig.consistency = True
defaultConfig.responseIsMarge = True
# conn = Connection.GetConnection(host,username="root", password="root",defaultConfig=defaultConfig)
# ret = conn.test()
# print(ret)

test = UltipaConnectionPool(host,username="root", password="root",defaultConfig=defaultConfig)

uqls = [
    "listUser()", #tables
    "show().edge_property()", #
    "show().node_property()",
    "find().nodes(1,2,3).select(*)",
    "find().edges(1,2,3).select(*)",
    "ab().src(12).dest(21).depth(5).limit(5).select(*)",
    "t().n(a).e().n(2).return(a.name,a.age)",
    "show().task()",
    "show().task()",
    "show().task()",
    "show().task()",
    "show().task()",
]

def asyncExecuteUql(uql: str):
    t = threading.current_thread()
    req = test.get_conn().uql(uql)
    print(t.getName() +" "+ uql + " " + req.toJSON())

def main():
    tpool = MPThreadPool(10)
    # tpool.map(asyncExecuteUql, uqls)
    tpool.starmap_async(asyncExecuteUql, (uqls,))
    # for i in uqls:
    #     tpool.apply_async(asyncExecuteUql,(i,))
    tpool.close()
    tpool.join()
    print("线程结束 Finished")



main()
