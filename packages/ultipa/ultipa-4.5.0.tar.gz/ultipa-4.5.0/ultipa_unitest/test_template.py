import unittest
from ultipa import ULTIPA_REQUEST
from ultipa_unitest import conn
class TestUltipaMethods(unittest.TestCase):
    #test 3.0
    gname = 'test_property'
    def test_search(self):
        't().n().e().n(n2).return(n2)'
        "t(p).n(a{type:'指导员'}).e(d).n({type:'老师'}).e().n(c{type:'学生'}).limit(100).return(c)"
        "t(p).n(n1).e(e).n(n2).return(p,n1,e,n2)"
        item1 = ULTIPA_REQUEST.TemplateNodeItem(name=ULTIPA_REQUEST.TNodeItem.n,alias='n1')
        item2 = ULTIPA_REQUEST.TemplateEdgeItem(name=ULTIPA_REQUEST.TEdgeItem.e,alias='e')
        item3 = ULTIPA_REQUEST.TemplateNodeItem(name=ULTIPA_REQUEST.TNodeItem.n,alias='n2')
        req = ULTIPA_REQUEST.Template(alias='p',items=[item1,item2,item3],limit=5,_return=['p','n1','e','n2'])
        ret = conn.template(request=req)
        print(ret.toJSON())