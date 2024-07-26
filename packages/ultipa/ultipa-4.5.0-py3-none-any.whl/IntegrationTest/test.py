
import unittest
from ultipa import *
from ultipa import Connection, ULTIPA_REQUEST, ULTIPA, FILTER
from ultipa_unitest import conn

ret = conn.getGraph(ULTIPA_REQUEST.GraphInfo(), RequestConfig())
ret = ret.toDict()
id = ret.get('data').get('totalNodes')
print(id)
