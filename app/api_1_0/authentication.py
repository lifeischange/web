# !/usr/bin/python
#coding:utf-8

from .errors import forbidden,unauthorized
from flask_httpauth import HTTPBasicAuth
from . import api
from flask import g,jsonify
from ..models import User,AnonymousUser

auth=HTTPBasicAuth()

@auth.verify_password
def verify_password(email_or_token,password):
	if email_or_token=="":
		g.current_user=AnonymousUser()
		return True
	if password=="":
		g.current_user=User.verify_auth_token(email_or_token)
		g.token_used=True
		return g.current_user is not None
	user=User.query.filter_by(email=email_or_token).first()
	if not user:
		return False
	g.current_user=user
	g.token_used=False
	return user.verify_password(password)
	user=User.query.filter_by(email=email).first()
	if not user:
		return False
	g.current_user=user
	return user.verify_password(password)

@auth.error_handler
def auth_error():
	return unauthorized(u"非法凭证")

@api.before_request
@auth.login_required
def before_request():
	if not g.current_user.is_anonymous and \
		not g.current_user.confirmed:
		return forbidden(u"未注册账户")

@api.route("/token")
def get_token():
	if g.current_user.is_anonymous or g.token_used:
		return unauthorized(u"非法凭证")
	return jsonify({"token":g.current_user.generate_auth_token(expiration=3600),"expiration":3600})
