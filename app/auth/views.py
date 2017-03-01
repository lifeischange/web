# !/usr/bin/python
# coding:utf-8

from . import auth
from flask import render_template,redirect,request,url_for,flash
from flask_login import login_user,logout_user,login_required
from ..models import User
from .forms import LoginForm,RegistrationForm
from datetime import datetime
from .. import db


@auth.route("/login",methods=["GET","POST"])
def login():
	form=LoginForm()
	if form.validate_on_submit():
		user=User.query.filter_by(email=form.email.data).first()
		if user==None:
			user=User.query.filter_by(username=form.email.data).first()
		if user is not None and user.verify_password(form.password.data):
			login_user(user,form.remember_me.data)
		return redirect(request.args.get("next") or url_for("main.index"))
		flash("Invalid username or password")
	return render_template("auth/login.html",form=form,current_time=datetime.utcnow())

@auth.route("/logout")
@login_required
def logout():
	logout_user()
	flash(u"你已经退出了。")
	return redirect(url_for("main.index"))

@auth.route("/register",methods=["POST","GET"])
def register():
	form=RegistrationForm()
	if form.validate_on_submit():
		user=User(username=form.username.data,
				  password=form.password.data,
				  email=form.email.data)
		db.session.add(user)
		flash(u"你可以进入了")
		return redirect(url_for("auth.login"))
	return render_template("auth/register.html",form=form,current_time=datetime.utcnow())
