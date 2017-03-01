# !/usr/bin/python
# coding:utf-8

from . import db#载入数据库
from werkzeug.security import generate_password_hash,check_password_hash #通过werkzeug中的security模块生产密码的哈\希值，这个值保存在数据库中。下次登录时，先使用密码生成散列值，在于数据库中的对比。数据库被模型函数隔离，不与用户发\生直接关系。
from flask_login import UserMixin#给数据模型增加用户登录模块

class User(UserMixin,db.Model):
	__tablename__="users"
	id=db.Column(db.Integer,primary_key=True)
	username=db.Column(db.String(64),unique=True,index=True)
	password_hash=db.Column(db.String(128))#字符串宽度128
	email=db.Column(db.String(64),unique=True,index=True)
	role_id=db.Column(db.Integer,db.ForeignKey("roles.id"))

	def __repr__(self):
		return "<Role %r>"%self.username

	@property
	def password(self):
		raise AttributeError(u"密码不可见")

	@password.setter
	def password(self,password):
		self.password_hash=generate_password_hash(password)

	def verify_password(self,password):
		return check_password_hash(self.password_hash,password)

class Role(db.Model):
	__tablename__="roles"
	id=db.Column(db.Integer,primary_key=True)
	name=db.Column(db.String(64),unique=True,index=True)
	users=db.relationship("User",backref="role")

	def __repr__(self):
		return "<User %s>"%self.name
#加载用户的回调函数
from . import login_manager#初始化时定义的登录模型

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

