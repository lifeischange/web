# !/usr/bin/python
# coding:utf-8

from . import auth
from flask import render_template,redirect,request,url_for,flash
from flask_login import login_user,logout_user,login_required,current_user
from ..models import User
from .forms import LoginForm,RegistrationForm,ChangePasswordForm,ChangeEmailForm
from datetime import datetime
from .. import db
from ..email import send_email

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
		flash(u"密码或用户名不正确")
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
		db.session.commit()
		token=user.generate_confirmation_token()
		send_email(user.email,"验证账号","auth/email/confirm",user=user,token=token)
		flash(u"验证链接已经发到你的邮箱了")
		return redirect(url_for("main.index"))
	return render_template("auth/register.html",form=form,current_time=datetime.utcnow())

@auth.route("/confirm/<token>")
@login_required
def confirm(token):
	if current_user.confirmed:
		return redirect(url_for("main.index"))
	if current_user.confirm(token):#模型函数
		flash(u"你已经成功注册。") 
	else:
		flash(u"链接已失效")
	return redirect(url_for("main.index"))

@auth.before_app_request
def before_request():
	if current_user.is_authenticated \
		and not current_user.confirmed\
		and request.endpoint[:5]!="auth."\
		and request.endpoint !="static":
		return redirect(url_for("auth.unconfirmed"))

@auth.route("/unconfirmed")
def unconfirmed():
	if current_user.is_anonymous or current_user.confirmed:
		return redirect(url_for("main.index"))
	return render_template("auth/unconfirmed.html",current_time=datetime.utcnow())

@auth.route("/confirm")
@login_required
def resend_confirmation():
	token=current_user.generate_confirmation_token()
	send_email(current_user.email,u"验证账户","auth/email/confirm",user=current_user,token=token)
	flash(u"一封新的认证邮件已经发送给你了")
	return redirect(url_for("main.index"))

@auth.route("/change-password",methods=["GET","POST"])
@login_required
def change_password():
	form=ChangePasswordForm()
	if form.validate_on_submit():
		if current_user.verify_password(form.old_password.data):
			current_user.password=form.password.data
			db.session.add(current_user)
			flash(u"密码已修改")
			return redirect(url_for("main.index"))
		else:
			flash(u"密码不正确")
	return render_template("auth/change_password.html",form=form,current_time=datetime.utcnow())

@auth.route("/reset",methods=["POST","GET"])
def password_reset_request():
	if not current_user.is_anonymous:
		return redirect(url_for("main.index"))
	form=PasswordResetRequestForm()
	if form.validate_on_submit():
		user=User.query.filter_by(email=form.email.data).first()
		if user:
			token=user.generate_reset_token()
			send_email(user.email,u"重置密码","auth/email/reset_password",user=user,token=token,
			next=request.args.get("index"))
		flash(u"一封重置密码的邮件已经发送到你的邮箱")
		return redirect(url_for("auth.login"))
	return render_template("auth/reset_password.html",form=form,current_time=datetime.utcnow())

@auth.route("/reset/<token>",methods=["POST","GET"])
def password_reset(token):
	if not current_user.is_anonymous:
		return redirect(url_for("main.index"))
	form=PasswordResetForm()
	if form.validate_on_submit():
		user=User.query.filter_by(email=form.email.data).first()
		if user is None:
			return redirect(url_for("main.index"))
		if user.reset_password(token,form.password.data):
			flash(u"密码已更新")
			return redirect(url_for("auth.login"))
		else:
			return redirect(url_for("main.index"))
	return render_template("auth/reset_password.html",form=form,current_time=datetime.utcnow())

@auth.route("/change-email",methods=["GET","POST"])
@login_required
def change_email_request():
	form=ChangeEmailForm()
	if form.validate_on_submit():
		if current_user.verify_password(form.password.data):
			new_email=form.email.data
			token=current_user.generate_email_change_token(new_email)
			send_email(new_email,u"确认你的邮箱地址","auth/email/change_email",user=current_user,token=token)
			flash(u"一封更改邮箱地址的邮件已经发送到你的邮箱，请注意查收")
			return redirect(url_for("main.index"))
		else:
			flash(u"邮箱地址或密码不正确")
	return render_template("auth/change_email.html",form=form,current_time=datetime.utcnow())

@auth.route("/change-email/<token>")
@login_required
def change_email(token):
	if current_user.change_email(token):
		flash(u"邮箱地址已更新")
	else:
		flash(u"非法请求")
	return redirect(url_for("main.index"))

@auth.before_app_request
def before_request():
	if current_user.is_authenticated:
		current_user.ping()
		if not current_user.confirmed \
			and request.endpoint[:5]!="auth":
			return redirect(url_for("auth.unconfirmed"))

