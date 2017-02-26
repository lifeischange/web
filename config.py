# !/usr/bin/python
# coding:utf-8

import os
basedir=os.path.abspath(os.path.dirname(__file__))

class config:#创造一个配置基类，不使用新式类
	SECRET_KEY=os.environ.get('SECRET_KEY') or "shiyishi"
	SQLALCHEMY_COMMIT_ON_TEARDOWN=True
	BLOG_SUBJECT_PREFIX="welcome"
	BLOG_SENDER="927491949@qq.com"
	BLOG_MAIL_ADMIN=os.environ.get("BLOG_ADMIN")
	

	@staticmethod
	def init_app(app):
		pass
		
class DevelopmentConfig(config):#开发环境配置
	DEBUG=True
	MAIL_SERVER='smtp.qq.com'
	MAIL_PORT=587
	MAIL_USERNAME=os.environ.get("MAIL_USERNAME")
	MAIL_PASSWORD=os.environ.get("MAIL_PASSWORD")
	SQLALCHEMY_DATABASE_URI="mysql://root:123@localhost:3306/dev"

class TestingConfig(config):
	TESTING=True
	SQLALCHEMY_DATABASE_URI="mysql://root:123@localhost:3306/test"

class ProductionConfig(config):
	SQLALCHEMY_DATABASE_URI="mysql://root:123@localhost:3306/blog"

Config={
	"development":DevelopmentConfig,
	"testing":TestingConfig,
	"production":ProductionConfig,
	"default":DevelopmentConfig
}
