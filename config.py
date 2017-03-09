# !/usr/bin/python
# coding:utf-8

import os
basedir=os.path.abspath(os.path.dirname(__file__))

class config:#创造一个配置基类，不使用新式类
	SECRET_KEY=os.environ.get('SECRET_KEY') or "shiyishi"
	SQLALCHEMY_COMMIT_ON_TEARDOWN=True
	BLOG_SUBJECT_PREFIX=u"欢迎"
	BLOG_SENDER="927491949@qq.com"
	BLOG_MAIL_ADMIN=os.environ.get("BLOG_ADMIN")
	FLASKY_POSTS_PER_PAGE=25	
	FLASKY_FOLLOWS_PER_PAGE=20
	SLOW_QUERY_TIME=0.5
	SQLALCHEMY_RECORD_QUERIES=True
	SSL_DISABLE=True

	@staticmethod
	def init_app(app):
		pass
		
class DevelopmentConfig(config):#开发环境配置
	DEBUG=True
	MAIL_USE_TLS=True
	MAIL_SERVER='smtp.qq.com'
	MAIL_PORT=587
	MAIL_USERNAME=os.environ.get("MAIL_USERNAME")
	MAIL_PASSWORD=os.environ.get("MAIL_PASSWORD")
	SQLALCHEMY_DATABASE_URI="mysql://root:123@localhost:3306/dev"

class TestingConfig(config):
	WTF_CSRF_ENABLED=False
	TESTING=True
	SQLALCHEMY_DATABASE_URI="mysql://root:123@localhost:3306/test"

class ProductionConfig(config):
	#SQLALCHEMY_DATABASE_URI="mysql://root:123@localhost:3306/blog"
	SQLALCHEMY_DATABASE_URI="sqlite:////"+os.path.join(basedir,"data.sqlite")
	@classmethod
	def init_app(cls,app):
		Config.init_app(app)

		import logging
		from logging.handlers import SMTPHandler
		credentials=None
		secure=None
		if getattr(cls,"MAIL_USERNAME",None) is not None:
			credentials=(cls.MAIL_USERNAME,cls.MAIL_PASSWORD)
			if getattr(cls,"MAIL_USE_TLS",None):
				secure=()
		mail_handler=SMTPHandler(
					mailhost=(cls.MAIL_USERNAME,cls.MAIL_PORT),
					fromaddr=cls.BLOG_SENDER,
					toaddrs=[cls.BLOG_MAIL_ADMIN], 
					subject=cls.BLOG_SUBJECT_PROFIX+u"程序错误",
					credentials=credentials,
					secure=secure)
		mail_handler.setLevel(logging.ERROR)
		app.logger.addHandler(mail_handler)

class HerokuConfig(ProductionConfig):
	SSL_DISABLE=bool(os.environ.get('SSL_DISABLE'))
	
	@classmethod
	def init_app(cls,app):
		ProductionConfig.init_app(app)

		import logging
		from logging import StreamHandler
		file_handler=StreamHandler()
		file_handler.setLevel(logging.WARNING)
		app.logger.addHandler(file_handler)
		
		from werkzeug.contrib.fixers import ProxyFix
		app.wsgi_app=ProxyFix(app.wsgi_app)
Config={
	"development":DevelopmentConfig,
	"testing":TestingConfig,
	"production":ProductionConfig,
	"default":DevelopmentConfig,
	"heroku":HerokuConfig
	
}
