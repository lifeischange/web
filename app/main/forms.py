# !/usr/bin/python
# coding:utf-8

from flask_wtf import Form
from wtforms import StringField,SubmitField,TextAreaField,SelectField,BooleanField
from wtforms.validators import Required,Length,Regexp,Email
from flask_pagedown.fields import PageDownField

class NameForm(Form):
	name=StringField(u"你的名字是",validators=[Required()])
	submit=SubmitField(u"提交")

class EditProfileForm(Form):
	name=StringField(u"昵称",validators=[Length(0,64)])
	location=StringField(u"坐标位置",validators=[Length(0,64)])
	about_me=TextAreaField(u"我的签名")
	submit=SubmitField(u"提交")

class EditProfileAdminField(Form):
	email=StringField(u"邮箱",validators=[Required(),Email(),Length(1,64)])
	username=StringField(u"用户名",validators=[Required(),Length(1,64),Regexp("^[a-zA-Z].*$",0,u"用户名必须是字母开头")])
	confirmed=BooleanField(u"验证")
	role=StringField(u"用户角色",coerce=int)
	name=StringField(u"昵称",validators=[Length(0,64)])
	location=StringField(u"坐标位置",validators=[Length(0,64)])
	about_me=TextAreaField(u"我的资料")
	submit=SubmitField(u"提交")

	def __init__(self,user,*args,**kwargs):
		super(EditProfileAdminField,self).__init__(*args,**kwargs)
		self.role.choices=[(role.id,role.name) for role in Role.query.order_by(Role.name).all()]
		self.user=user

	def validate_email(self,field):
		if field.data !=self.user.email and \
			User.query.filter_by(email=field.data).first():
				raise ValidationError(u"邮箱已被注册")

	def validate_username(self,field):
		if field.data != self.user.username and \
			User.query.filter_by(username=field.data).first():
				raise ValidationError(u"用户名已被注册")

class PostForm(Form):
	body=PageDownField(u"你的想法",validators=[Required()])
	submit=SubmitField(u"上传")
