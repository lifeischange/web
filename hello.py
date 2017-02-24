# !/usr/bin/dev/python
# coding:utf-8

from flask import Flask,render_template
from flask_script import Manager
from flask_moment import Moment
from flask_bootstrap import Bootstrap
from datetime import datetime
from flask_wtf import Form
from wtforms import StringField,SubmitField
from wtforms.validators import Required

app=Flask(__name__)
manager=Manager(app)
moment=Moment(app)
bootstrap=Bootstrap(app)

app.config['SECRET_KEY']='hard to guess' 

class NameForm(Form):
	name=StringField(u"我的名字",validators=[Required()])
	submit=SubmitField(u"提交")

@app.route("/",methods=['GET','POST'])
def index():
	name=None
	form=NameForm()
	if form.validate_on_submit():
		name=form.name.data
		form.name.data=''
	return render_template("base.html",form=form,current_time=datetime.utcnow())

@app.route("/user/<name>")
def user(name):
	form=NameForm()
	if form.validate_on_submit():
		name=form.name.data
		form.name.data=''
	return render_template("base.html",name=name,form=form,current_time=datetime.utcnow())


if __name__=="__main__":
    manager.run()
