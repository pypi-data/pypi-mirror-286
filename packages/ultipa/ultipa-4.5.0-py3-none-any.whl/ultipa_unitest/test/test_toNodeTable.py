
from ultipa.utils.format import FormatType

#
# headers = [{"name": "id", "type": "PROPERTY_INT32"}, {"name": "name", "type": "PROPERTY_STRING"},
#            {"name": "age", "type": "PROPERTY_INT32"}]
# results = [{"id": "1000001", "name": "Debra Wheeler", "age": "34"}]
# ret = FormatType.toNodeTable(headers=headers,rows=results)
# print(ret.headersList)
# print(ret.nodeRowsList)


# headers = [{"name": "id", "type": "PROPERTY_INT32"}, {"name": "from_id", "type": "PROPERTY_INT32"},
#            {"name": "to_id", "type": "PROPERTY_INT32"},{"name": "name", "type": "PROPERTY_STRING"}]
# results = [{"id": "1000001", "from_id": "1","to_id":'2',"name": "test"}]
# ret = FormatType.toEdgeTable(headers=headers,rows=results)
# print(ret.headersList)
# print(ret.edgeRowsList)