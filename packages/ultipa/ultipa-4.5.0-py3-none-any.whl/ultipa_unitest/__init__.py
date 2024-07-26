
from ultipa_unitest.helper import GetTestConnection
import random
# host = None

# host = ["39.99.246.64:60069","39.99.246.64:60068"] #
# host = "192.168.3.160:60062"  # 自己虚拟机
# host = "192.168.3.253:60064"  # 自己虚拟机

# host = "192.168.3.129:60062" #amz
# host = '192.168.3.129:60066' #alimama
# host = '192.168.3.129:60064' #gongshang
# host = "39.99.246.64:60068" #AI
# host = "39.99.246.64:60064" #gongshang
# host = "192.168.3.204:60061" #gongshang
# host = "192.168.3.160:60061" #gongshang
# host = ["192.168.1.83:60061"] #fanzhi
# host = ["192.168.1.91:60061"] #fanzhi
# host = ["210.13.32.146:40101"] #fanzhi
# host = ["210.13.32.146:60099"] #fanzhi
# host = ["www.ultipa.com:60099"] #fanzhi
# host = ["192.168.1.85:61231"] #fanzhi
# host = ["20.232.103.92:60061"] #fanzhi
# host = ["192.168.1.85:60601","192.168.1.87:60601","192.168.1.88:60601"] #fanzhi
# host = ["192.168.1.85:64801","192.168.1.85:64802","192.168.1.85:64803"] #fanzhi
# host = ["192.168.1.85:64801", "192.168.1.85:64802", "192.168.1.85:64803"] #fanzhi
host = ["3.12.242.20:60063"] #fanzhi
# host = ["192.168.1.85:60601","192.168.1.87:60601","192.168.1.88:60601"]
# host = ["192.168.1.65:60061"] #fanzhi
# host = ["68.79.42.185:60061","68.79.56.245:60061","52.82.52.195:60061"] #fanzhi
# print(host)
username="root"
pwd="root"
conn = GetTestConnection(host=host,logFileName="test.log",isWriteToFile=True,user=username,pwd=pwd)
