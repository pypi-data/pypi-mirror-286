import unittest
from ultipa import Connection,ULTIPA_REQUEST,ULTIPA
from ultipa_unitest import conn


class TestUltipaMethods(unittest.TestCase):

    def test_get_usersetting(self):
        ret = conn.getUserSetting(ULTIPA_REQUEST.GetUserSetting(username='ultipa',type='user_info'))
        print(ret.toJSON())

    def test_set_usersetting(self):
        ret = conn.setUserSetting(ULTIPA_REQUEST.SetUserSetting(username='ultipa',type='user_info',data='test'))
        print(ret.toJSON())
