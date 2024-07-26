import unittest
from ultipa import Connection
from ultipa import UltipaConfig

def GetTestConnection(host: str = None,crtFilePath:str=None) -> Connection:
    host = host and host or "192.168.3.129:60062"
    defaultConfig = UltipaConfig()
    defaultConfig.responseWithRequestInfo=True
    conn = Connection(host=host, username="root", password="root", crtFilePath=crtFilePath,defaultConfig=defaultConfig)
    return conn


class TestUltipaMethods(unittest.TestCase):

    def test_secure(self,):
        conn = GetTestConnection('192.168.3.129:60062', "./ultipa.crt")
        node_ret = conn.test()
        print(node_ret)

    def test_insecure(self, ):
        conn = GetTestConnection('192.168.3.129:60062')
        node_ret = conn.test()
        print(node_ret)


