import unittest
from ultipa import *
from ultipa import Connection, ULTIPA_REQUEST, ULTIPA
from ultipa.structs import GraphInfo
from ultipa.structs.Property import Property
from ultipa.structs.PropertyType import PropertyTypeStr
from ultipa_unitest import conn


class TestUltipaMethods(unittest.TestCase):
    graphSetName = 'default'

    # 4.0
    conn = conn
    
    def test_getproperty(self):
        ret = conn.getProperty(dbType=DBType.DBNODE,schema="default")
        print(ret.toJSON())


    def test_show_schema(self):
        conn.defaultConfig.setDefaultGraphName(self.graphSetName)
        uql = "show().property()"
        ret = conn.uql(uql)
        print(ret.toJSON())
        # print(ret.alias("_nodeProperty").asProperties())
        # ret.Print()

    def test_listproperty(self):
        '''
        :return:
        '''
        # ret = conn.createGraph(ULTIPA_REQUEST.CreateGraph('test_property'))
        # print(ret.toJSON())
        conn.defaultConfig.setDefaultGraphName(self.graphSetName)
        ret = conn.showProperty()
        print(ret.Print())
        # print(ret.alias("_nodeProperty").asProperties()[0].lte)        # print(ret)
        # print(ret.get(0).asTable().toDicts())

        # print(ret.toJSON())
        # print(ret.data[0].data[0].type)
        # ret.Print()
        # print(ret.data[0].data.propertyName)
        # properList = []
        # for pro in ret.data:
        #     for i in pro.data:
        #         properList.append(i.propertyName)
        # print(properList)
        # ret = conn.listProperty()
        # conn.defaultConfig.defaultGraph = "amz"
        # ret = self.conn.showProperty()
        # ret.data[1].data[0].
        # ret = self.conn.uql("show().property()")
        # for i in ret.data:
        #     for j in i.data:
        #         print(j.toJSON())
        # print(ret.data[0].data[0].propertyName)
        # print(ret.data[0].data[0].schema)
        # print(ret.data[0].data[0].propertyType)
        # conn.defaultConfig.defaultGraph = "ultipa_www"
        # ret1 = self.conn.showProperty()
        # print(ret1.toJSON())

        # ret = self.conn.getProperty(ULTIPA_REQUEST.GetProperty(type=DBType.DBNODE, schema="default"))
        # # print(ret.data[0])
        # print(ret.toJSON())
        # print(ret.Print())

        # ret = self.conn.alterProperty(ULTIPA_REQUEST.AlterProperty(DBType.DBNODE,ULTIPA_REQUEST.CommonSchema("test","test"),"test1"))
        # print(ret.toJSON())

        # ret = self.conn.alterProperty(ULTIPA_REQUEST.AlterProperty(DBType.DBEDGE,
        #                                                       ULTIPA_REQUEST.CommonSchema("test", "test"), "test1"))

        # ret = conn.showSchema(ULTIPA_REQUEST.ShowSchema(schemaType=DBType.DBEDGE))
        # print(ret.toJSON())
        # ret = conn.showProperty()
        # conn.defaultConfig.defaultGraph = "ultipa_www"
        # ret = conn.getProperty(ULTIPA_REQUEST.GetProperty(DBType.DBNODE))
        # print(ret.toJSON())

    #
    # # 4.0
    def test_createNodeproperty_decimal(self):
        # self.create_schema(self.graphSetName, 'test', DBType.DBNODE)
        # self.create_schema(self.graphSetName, 'test', DBType.DBEDGE)
        # createProperty = Property("@@{}",type=PropertyTypeStr.PROPERTY_STRING)
        createProperty = Property("decimal", type=PropertyTypeStr.PROPERTY_DECIMAL(30,20))
        conn.defaultConfig.setDefaultGraphName(self.graphSetName)
        ret = conn.createProperty(dbType=DBType.DBNODE,schemaName="default",prop=createProperty)
        print(ret.toJSON())
        # self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)
    def test_createNodeproperty_set(self):
        # self.create_schema(self.graphSetName, 'test', DBType.DBNODE)
        # self.create_schema(self.graphSetName, 'test', DBType.DBEDGE)
        # createProperty = Property("@@{}",type=PropertyTypeStr.PROPERTY_STRING)
        createProperty = Property("test_set", type=PropertyTypeStr.PROPERTY_SET,subTypes=[PropertyTypeStr.PROPERTY_STRING])
        conn.defaultConfig.setDefaultGraphName(self.graphSetName)
        ret = conn.createProperty(dbType=DBType.DBNODE,schemaName="test_set",prop=createProperty)
        print(ret.toJSON())
    def test_createNodeproperty_list(self):
        # self.create_schema(self.graphSetName, 'test', DBType.DBNODE)
        # self.create_schema(self.graphSetName, 'test', DBType.DBEDGE)
        createProperty = Property("nodx","test_list_111",type=PropertyTypeStr.PROPERTY_LIST,subTypes=[PropertyTypeStr.PROPERTY_STRING])
        conn.defaultConfig.setDefaultGraphName(self.graphSetName)
        ret = conn.createProperty(dbType=DBType.DBNODE,prop=createProperty)
        print(ret.toJSON())

    #
    # 4.0
    def test_createEdgeproperty(self):
        createProperty = Property("edgx", "test_create_nodeproperty")
        conn.defaultConfig.setDefaultGraphName(self.graphSetName)
        ret = conn.createProperty(dbType=DBType.DBEDGE, prop=createProperty)
        print(ret.toJSON())
        # self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)

    # 4.0
    def test_dropProperty(self):
        ret = conn.dropProperty()
        print(ret.toJSON())

    def test_alterProperty(self):
        conn.defaultConfig.defaultGraph = self.graphSetName
        ret = conn.alterProperty(DBType.DBNODE,schema="nodx",property="test_create_nodeproperty",newProperty="test_create_nodeproperty_111")
        print(ret.toJSON())
        self.assertEqual(ret.status.code, ULTIPA.Code.SUCCESS)

    def test_property_flow(self):
        graphName = 'pytest'
        strname = 'test_str'
        int32name = 'test_int'
        uint32name = 'test_uint32'
        int64name = 'test_int64'
        uint64name = 'test_uint64'
        floatname = 'test_float'
        doublename = 'test_double'
        timename = 'test_DateTime'
        listname = 'test_list'

        propertyList = [
            {'name': strname, 'type': PropertyTypeStr.PROPERTY_STRING, 'description': 'test_str'},
            {'name': int32name, 'type': PropertyTypeStr.PROPERTY_INT, 'description': 'test_int'},
            {'name': uint32name, 'type': PropertyTypeStr.PROPERTY_UINT32, 'description': 'test_uint32'},
            {'name': int64name, 'type': PropertyTypeStr.PROPERTY_INT64, 'description': 'test_int64'},
            {'name': uint64name, 'type': PropertyTypeStr.PROPERTY_UINT64, 'description': 'test_uint64'},
            {'name': floatname, 'type': PropertyTypeStr.PROPERTY_FLOAT, 'description': 'test_float'},
            {'name': doublename, 'type': PropertyTypeStr.PROPERTY_DOUBLE, 'description': 'test_double'},
            {'name': timename, 'type': PropertyTypeStr.PROPERTY_DATETIME, 'description': 'test_DateTime'},
            {'name': listname, 'type': PropertyTypeStr.PROPERTY_LIST,"subType":[PropertyTypeStr.PROPERTY_STRING], 'description': 'test_list'},
        ]

        ret = conn.createGraph(GraphInfo(graphName))
        assert ret.status.code == ULTIPA.Code.SUCCESS, ret.toJSON()
        self.conn.defaultConfig.defaultGraph = graphName
        # self.create_schema(graphName, 'test', DBType.DBNODE)
        # self.create_schema(graphName, 'test', DBType.DBEDGE)

        for property in propertyList:
            createProperty = Property("test", property.get("name"),type=property.get("type"),description=property.get("description"),subTypes=property.get("subType"))
            ret = self.conn.createProperty(dbType=DBType.DBNODE,prop=createProperty)
            assert ret.status.code == ULTIPA.Code.SUCCESS, ret.toJSON()

            ret = self.conn.createProperty(dbType=DBType.DBEDGE,prop=createProperty)
            assert ret.status.code == ULTIPA.Code.SUCCESS, ret.toJSON()

        ret = self.conn.showProperty(requestConfig=RequestConfig(graphName=graphName))
        for props in ret.data:
            assert len(props.data) == 9, props.toJSON()
            for data in props.data:
                if data.type == PropertyTypeStr.PROPERTY_STRING:
                    assert data.name == strname
                elif data.type == PropertyTypeStr.PROPERTY_INT:
                    assert data.name == int32name

                elif data.type == PropertyTypeStr.PROPERTY_UINT32:
                    assert data.name == uint32name

                elif data.type == PropertyTypeStr.PROPERTY_INT64:
                    assert data.name == int64name

                elif data.type == PropertyTypeStr.PROPERTY_UINT64:
                    assert data.name == uint64name

                elif data.type == PropertyTypeStr.PROPERTY_FLOAT:
                    assert data.name == floatname

                elif data.type == PropertyTypeStr.PROPERTY_DOUBLE:
                    assert data.name == doublename

                elif data.type == PropertyTypeStr.PROPERTY_DATETIME:
                    assert data.name == timename
                elif data.type == PropertyTypeStr.PROPERTY_LIST:
                    assert data.name == listname
