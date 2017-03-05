# !/bin/python
# coding:utf-8

from flask import Flask,render_template
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_login import LoginManager#登录用户管理模块
from flask_pagedown import PageDown

bootstrap=Bootstrap()
mail=Mail()
moment=Moment()
db=SQLAlchemy()
pagedown=PageDown()

login_manager=LoginManager()
login_manager.session_protection="strong"
login_manager.login_view="auth.login"

def create_app(config_name):
	app=Flask(__name__)
	app.config.from_object(Config[config_name])
	Config[config_name].init_app(app)
	
	login_manager.init_app(app)#扩展通用模式

	bootstrap.init_app(app)
	mail.init_app(app)
	moment.init_app(app)
	db.init_app(app)
	pagedown.init_app(app)

	from .main import main as main_blueprint
	app.register_blueprint(main_blueprint)
	
	from .auth import auth as auth_blueprint
	app.register_blueprint(auth_blueprint,url_perfix='/auth')

	return app

