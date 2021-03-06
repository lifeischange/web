# !/usr/bin/env python
# coding:utf-8

import unittest
from app.models import User,Role,AnonymousUser,Permission

class Usermodeltestcase(unittest.TestCase):
	def test_password_setter(self):#测试说明创建的用户的密码散列值是存在的
		u=User(password="elephant")
		self.assertTrue(u.password_hash is not None)

	def test_password_getter(self):#断言查询密码会出现属性错误
		u=User(password="bullet")
		with self.assertRaises(AttributeError):
			u.password

	def test_password_verification(self):#验证散列值有效
		u=User(password="bullet")
		self.assertTrue(u.verify_password("bullet"))
		self.assertFalse(u.verify_password("bull"))

	def test_password_salts_are_random(self):
		u=User(password="bullet")
		u2=User(password="bullet")
		self.assertTrue(u.password_hash!=u2.password_hash)
	
	def test_roles_and_permissions(self):
		Role.insert_roles()
		u=User(email="123@321.com",password="cat")
		self.assertTrue(u.can(Permission.WRITE_ARTICLES))
		self.assertFalse(u.can(Permission.MODERATE_COMMENTS))

	def test_anonymous_user(self):
		u=AnonymousUser()
		self.assertFalse(u.can(Permission.FOLLOW))
