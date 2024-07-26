from ultipa import Connection, UltipaConfig,ULTIPA_RESPONSE,ULTIPA_REQUEST,ULTIPA
conn = Connection(host='124.193.211.21:63163', username="root", password="root")
conn.defaultConfig.defaultGraph = 'test_str'
conn.defaultConfig.responseWithRequestInfo=True
ret = conn.createProperty(ULTIPA_REQUEST.CreateProperty(type=DBType.DBNODE, name='name',
                                                 property_type=ULTIPA.PropertyType.PROPERTY_STRING, description='test'))

# ret = conn.insertNode(ULTIPA_REQUEST.InsertNode(nodes=[{'name': 'test'}]))
print(ret.toJSON())