# !/usr/bin/env python
# coding:utf-8

from flask_wtf import Form
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import Required,Length,Email,Regexp,EqualTo #约束条件
from wtforms import ValidationError
from ..models import User

class LoginForm(Form):
	email=StringField(u"用户名/邮箱",validators=[Required(),Length(1,64)])
	password=PasswordField(u"密码",validators=[Required()])
	remember_me=BooleanField(u"记住我")
	submit=SubmitField(u"登录")

#注册表单
class RegistrationForm(Form):
	email=StringField(u"邮箱",validators=[Required(),Length(1,64),Email()])
	username=StringField(u"用户名",validators=[Required(),Length(1,64),Regexp("^[a-zA-Z].*$",0)])
	password=StringField(u"密码",validators=[Required(),EqualTo("password2",message=u"密码不一致")])
	password2=StringField(u"密码确认",validators=[Required()])
	submit=SubmitField(u"注册")

	def validate_email(self,field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError(u"邮箱已存在")

	def validate_username(self,field):
		if User.query.filter_by(username=field.data).first():
			raise ValidationError(u"用户名已存在")
		
