# !/usr/bin/dev/python
# coding:utf-8

import os
from flask import Flask,render_template,redirect,session,url_for,flash
from flask_script import Manager,Shell
from flask_moment import Moment
from flask_bootstrap import Bootstrap
from datetime import datetime
from flask_wtf import Form
from wtforms import StringField,SubmitField
from wtforms.validators import Required
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate,MigrateCommand
from flask_mail import Mail,Message
from threading import Thread

basedir=os.path.abspath(os.path.dirname(__file__))

app=Flask(__name__)
manager=Manager(app)
moment=Moment(app)
bootstrap=Bootstrap(app)

app.config['SECRET_KEY']='hard to guess' 
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:123@localhost:3306/flask'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True

app.config['MAIL_SERVER']="smtp.qq.com"
app.config['MAIL_PORT']=465
app.config['MAIL_USE_SSL']=True
app.config['MAIL_USERNAME']=os.environ.get("MAIL_USERNAME")
app.config['MAIL_PASSWORD']=os.environ.get("MAIL_PASSWORD")

app.config['FLASKY_ADMIN']=os.environ.get("FLASKY_ADMIN")

app.config['MAIL_SUBJECT']='FLASKY'
app.config['MAIL_SENDER']="927491949@qq.com"
db=SQLAlchemy(app)
migrate=Migrate(app,db)
manager.add_command('db',MigrateCommand)

mail=Mail(app)

class Role(db.Model):
	__tablename__='roles'
	id=db.Column(db.Integer,primary_key=True)
	name=db.Column(db.String(64),unique=True)
	users=db.relationship('User',backref='role')

	def __repr__(self):
		return 'Role %r'%self.name

class User(db.Model):
	__tablename__='users'
	id=db.Column(db.Integer,primary_key=True)
	username=db.Column(db.String(64),unique=True,index=True)
	role_id=db.Column(db.Integer,db.ForeignKey('roles.id'))

	def __repr__(self):
		return 'User %r'%self.username


class NameForm(Form):
	name=StringField(u"我的名字",validators=[Required()])
	submit=SubmitField(u"提交")

def make_shell_context():
	return dict(app=app,db=db,User=User,Role=Role)
manager.add_command("shell",Shell(make_context=make_shell_context))

def senf_async_email(app,msg):
	with app.app_context():
		mail.send(msg)
def send_mail(to,subject,template,**kwargs):
	msg=Message(app.config["MAIL_SUBJECT"]+subject,sender=app.config["MAIL_SENDER"],recipients=[to])
	msg.body=render_template(template+".txt",**kwargs)
	msg.html=render_template(template+".html",**kwargs)
	thr=Thread(target=senf_async_email,args=[app,msg])
	thr.start()
	return thr

@app.route("/",methods=['GET','POST'])
def index():
	form=NameForm()
	if form.validate_on_submit():
		user=User.query.filter_by(username=form.name.data).first()
		if user is None:
			user=User(username=form.name.data)
			db.session.add(user)
			session['Known']=False
			if app.config["FLASKY_ADMIN"]:
				send_mail(app.config["FLASKY_ADMIN"],"New User","mail/new_user",user=user)

		else:
			session['known']=True 
		old_name=session.get('name')
		if old_name is not None and old_name!=form.name.data:
			flash(u"你是不是改名字了？")
		session['name']=form.name.data
		form.name.data=''
		return redirect(url_for('index'))
	return render_template("base.html",known=session.get('known',False) ,name=session.get('name') ,form=form,current_time=datetime.utcnow())

@app.route("/user/<name>")
def user(name):
	form=NameForm()
	if form.validate_on_submit():
		name=form.name.data
		form.name.data=''
	return render_template("base.html",name=name,form=form,current_time=datetime.utcnow())


if __name__=="__main__":
    manager.run()
