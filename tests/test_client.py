# !/usr/env/python
#coding:utf-8

import re
import unittest
from flask import url_for
from app import create_app, db
from app.models import User, Role

class FlaskClientTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        response = self.client.get(url_for('main.index'))
        self.assertTrue(u"朋友".encode("utf-8") in response.data)

    def test_register_and_login(self):
        response = self.client.post(url_for('auth.register'), data={
            'email': 'john@example.com',
            'username': 'john',
            'password': 'cat',
            'password2': 'cat'
        })
        self.assertTrue(response.status_code == 302)

        response = self.client.post(url_for('auth.login'), data={
            'email': 'john@example.com',
            'password': 'cat'
        }, follow_redirects=True)
        self.assertTrue(re.search(u"你好".encode("utf-8"), response.data))
        self.assertTrue(
            u'你还没有激活你的账户'.encode('utf-8') in response.data)

        
        user = User.query.filter_by(email='john@example.com').first()
        token = user.generate_confirmation_token()
        response = self.client.get(url_for('auth.confirm', token=token),
                                   follow_redirects=True)
        self.assertTrue(
            u'你已经成功注册。'.encode('utf-8') in response.data)

        
        response = self.client.get(url_for('auth.logout'), follow_redirects=True)
        self.assertTrue(u'你已经退出了。'.encode('utf-8') in response.data)
