import os
import unittest

from ultipa.configuration.InsertConfig import InsertConfig
from ultipa.structs import DBType, InsertType
from ultipa_unitest import GetTestConnection
from ultipa import Connection, ULTIPA_REQUEST, ULTIPA

# host = ["192.168.1.87:60699"]
host = ["39.104.21.70:60699"]
conn = GetTestConnection(host=host, logFileName="test.log", isWriteToFile=False)


class news:
    def __init__(self, bannerImgUrl, content, create_time, description, indexImgUrl, order, publish_time, status,
                 title):
        self.bannerImgUrl = bannerImgUrl
        self.content = content
        self.create_time = create_time
        self.description = description
        self.indexImgUrl = indexImgUrl
        self.order = order
        self.publish_time = publish_time
        self.status = status
        self.title = title


class doc_tree:
    def __init__(self, create_time,order,parent_id,status,title):
        self.create_time = create_time
        self.order = order
        self.parent_id = parent_id
        self.status = status
        self.title = title
class Doc:
    def __init__(self,content,create_time,description,index_img,order,publish_time,status,title,tree_id,type):
        self.create_time = create_time
        self.content = content
        self.description = description
        self.index_img = index_img
        self.order = order
        self.publish_time = publish_time
        # self.treeChain = treeChain
        self.parent_id = tree_id
        self.status = status
        self.title = title
        self.type = type

class User:
    def __init__(self,username,password,email,company_email,phone,nickname,icon_url,status,create_time,company,industry,area):
        self.username = username
        self.password = password
        self.email = email
        self.company_email = company_email
        self.phone = phone
        self.nickname = nickname
        # self.treeChain = treeChain
        self.icon_url = icon_url
        self.status = status
        self.company = company
        self.create_time = create_time
        self.industry = industry
        self.area = area

class Langedge:
    def __init__(self,from_id,to_id,name):
        self._from_uuid=from_id
        self._to_uuid=to_id
        # self.name=name


class TestUltipaMethods(unittest.TestCase):
    gname = 'default'

    # def test(self):
    #     ret = conn.test()
    #     print(ret)

    def read_csv(self, file_path):
        import csv
        f = csv.reader(open(file_path, 'r', encoding='utf-8'))
        return f

    # 4.0
    def test_news(self):
        conn.defaultConfig.defaultGraph='ultipa_www'
        node_list = []
        f = self.read_csv(r"F:\ultipa.cn_data_3.0\new_nodes.csv")
        header = ",".join(f.__next__())
        print(header)
        for i in f:
            _id, bannerImgUrl, content, create_time, description, indexImgUrl, lang_id, open_level, order, publish_time, status, title, type = i
            node = news(bannerImgUrl, content, create_time, description, indexImgUrl, order, publish_time, status,
                        title).__dict__
            # conn.insertNodesBulk(ULTIPA_REQUEST.InsertNodeBulk(rows=[]))
            ret = conn.insertNode(ULTIPA_REQUEST.InsertNode(nodes=[node],schemaName="news"))
            print(ret.toJSON())
            if lang_id:
                ret = conn.insertEdge(ULTIPA_REQUEST.InsertEdge(edges=[Langedge(ret.data[0],int(lang_id),name="news").__dict__],schemaName='news_lang'))
                print(ret.toJSON())


    def test_doc_tree(self):
        conn.defaultConfig.defaultGraph='ultipa_www'
        f = self.read_csv(r"F:\ultipa.cn_data_3.0\new_nodes.csv")
        header = ",".join(f.__next__())
        print(header)
        for i in f:
            _id,create_time,lang_id,order,parent_id,status,title = i
            node = doc_tree(create_time,order,parent_id,status,title).__dict__
            # conn.insertNodesBulk(ULTIPA_REQUEST.InsertNodeBulk(rows=[]))
            ret = conn.insertNode(ULTIPA_REQUEST.InsertNode(nodes=[node],schemaName="docs"))
            print(ret.toJSON())
            if lang_id:
                ret = conn.insertEdge(ULTIPA_REQUEST.InsertEdge(edges=[Langedge(ret.data[0],int(lang_id),name="docs").__dict__],schemaName='docs_tree_lang'))
                print(ret.toJSON())

    def test_docs(self):
        conn.defaultConfig.defaultGraph='ultipa_www'
        f = self.read_csv(r"F:\ultipa.cn_data_3.0\doc_nodes.csv")
        header = ",".join(f.__next__())
        print(header)
        for i in f:
            _id,content,create_time,description,index_img,lang_id,order,publish_time,status,title,treeChain,tree_id,type = i
            node = Doc(content,create_time,description,index_img,order,publish_time,status,title,tree_id,type).__dict__
            # conn.insertNodesBulk(ULTIPA_REQUEST.InsertNodeBulk(rows=[]))
            ret = conn.insertNode(ULTIPA_REQUEST.InsertNode(nodes=[node],schemaName="docs"))
            print(ret.toJSON())
            if lang_id:
                if ',' in lang_id:
                    lang_id=lang_id.split(',')
                    for lang in lang_id:
                        ret = conn.insertEdge(ULTIPA_REQUEST.InsertEdge(edges=[Langedge(ret.data[0],int(lang),name="docs").__dict__],schemaName='docs_lang'))
                else:
                    ret = conn.insertEdge(
                        ULTIPA_REQUEST.InsertEdge(edges=[Langedge(ret.data[0], int(lang_id), name="docs").__dict__],
                                                  schemaName='docs_lang'))
                print(ret.toJSON())

    def test_users(self):
        conn.defaultConfig.defaultGraph='ultipa_www'
        f = self.read_csv(r"F:\ultipa.cn_data_3.0\user_nodes.csv")
        header = ",".join(f.__next__())
        print(header)
        for i in f:
            _id,username,password,email,company_email,phone,nickname,icon_url,status,create_time,company,industry,area = i
            node = User(username,password,email,company_email,phone,nickname,icon_url,status,create_time,company,industry,area).__dict__
            # conn.insertNodesBulk(ULTIPA_REQUEST.InsertNodeBulk(rows=[]))
            ret = conn.insertNode(ULTIPA_REQUEST.InsertNode(nodes=[node],schemaName="docs"))
            print(ret.toJSON())
            if lang_id:
                if ',' in lang_id:
                    lang_id=lang_id.split(',')
                    for lang in lang_id:
                        ret = conn.insertEdge(ULTIPA_REQUEST.InsertEdge(edges=[Langedge(ret.data[0],int(lang),name="docs").__dict__],schemaName='docs_lang'))
                else:
                    ret = conn.insertEdge(
                        ULTIPA_REQUEST.InsertEdge(edges=[Langedge(ret.data[0], int(lang_id), name="docs").__dict__],
                                                  schemaName='docs_lang'))
                print(ret.toJSON())

    def test_csv(self):
        self.read_csv(r"F:\ultipa.cn_data_3.0\new_nodes.csv")


    def test_graph_file(self):
        conn.defaultConfig.defaultGraph="ultipa_www"
        with open("./create_graph_ultipa_www.uql","r") as f:
            for line in f:
                if line.startswith("/"):
                    continue
                else:
                    conn.uql(line)

    def test_graph_www_data(self):
        conn_4_3 = GetTestConnection(host=host, logFileName="test.log", isWriteToFile=False)
        conn_4_3.defaultConfig.defaultGraph="ultipa_www"
        folder_path = "/Users/ultipa/work/ultipa-python-sdk2/ultipa_unitest/DBdata4.0/nodes"
        file_list = os.listdir(folder_path)
        for f in file_list:
            print(f)
            schema, _, _ = f.split(".")
            ret = conn_4_3._InsertByCSV(os.path.join(folder_path,f),DBType.DBNODE,InsertConfig(InsertType.UPSERT),schema)
            print(f,ret.status.message)
            if(ret.status.code==0):
                print("Success:"+folder_path)
            #     os.remove(os.path.join(folder_path,f))



    def test_graph_www_edge_data(self):
        conn_4_3 = GetTestConnection(host=host, logFileName="test.log", isWriteToFile=False)
        conn_4_3.defaultConfig.defaultGraph="ultipa_www"
        folder_path = "/Users/ultipa/work/ultipa-python-sdk2/ultipa_unitest/DBdata4.0/edges"
        file_list = os.listdir(folder_path)
        for f in file_list:
            print(f)
            schema, _, _ = f.split(".")
            ret = conn_4_3._InsertByCSV(os.path.join(folder_path,f),DBType.DBEDGE,InsertConfig(InsertType.UPSERT),schema)
            print(f,ret.status.message)
            if(ret.status.code==0):
                print("Success:"+folder_path)

                # os.remove(os.path.join(folder_path,f))

