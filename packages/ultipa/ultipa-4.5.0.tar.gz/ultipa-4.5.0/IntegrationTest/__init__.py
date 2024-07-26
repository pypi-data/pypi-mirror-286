from ultipa_unitest.helper import GetTestConnection
import random
host = None

# host = ["39.99.246.64:60069","39.99.246.64:60068"] #
# host = "192.168.3.160:60062"  # 自己虚拟机
# host = "192.168.3.253:60064"  # 自己虚拟机

# host = "192.168.3.129:60062" #amz
# host = '192.168.3.129:60066' #alimama
# host = '192.168.3.129:60064' #gongshang
# host = "39.99.246.64:60068" #AI
# host = "39.99.246.64:60064" #gongshang
# host = "192.168.3.204:60061" #gongshang
# host = "192.168.3.220:60061" #gongshang
# host = "192.168.3.129:60062" #fanzhi
print(host)
conn = GetTestConnection(host=host)