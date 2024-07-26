from ultipa import Connection
from ultipa import UltipaConfig
from ultipa.utils.logger import LoggerConfig


def GetTestConnection(host: list = None, crtFilePath=None, logName: str = 'test', logFileName: str = None,
					  isWriteToFile: bool = False,user="root",pwd = "root") -> Connection:
	host = host and host or ["124.193.211.21:60162"]
	defaultConfig = UltipaConfig()
	defaultConfig.responseWithRequestInfo = True
	defaultConfig.consistency = False
	defaultConfig.responseIsMarge = True
	defaultConfig.hosts = host
	defaultConfig.username = user
	defaultConfig.password = pwd
	defaultConfig.heartBeat=-1
	defaultConfig.uqlLoggerConfig=None
	if logFileName:
		defaultConfig.uqlLoggerConfig = LoggerConfig(name=logName, fileName=logFileName, isWriteToFile=isWriteToFile,
													 isStream=True)
	if crtFilePath:
		conn = Connection(host=host, crtFilePath=crtFilePath, defaultConfig=defaultConfig)
	else:
		# conn = Connection(host=host, username="root", password="root",defaultConfig=defaultConfig)
		conn = Connection.NewConnection(defaultConfig=defaultConfig)

	return conn
