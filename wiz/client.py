#!/usr/bin/env python
#coding:utf-8
# Author        : tuxpy
# Email         : q8886888@qq.com.com
# Last modified : 2015-11-02 10:49:06
# Filename      : client.py
# Description   : 
from __future__ import print_function, unicode_literals

from wiz import e, utils
from wiz.api import api_request
from wiz.notebook import NotebookManager
from wiz.auth import AuthManager

__all__ = ['Wiz']

class Wiz(object):
    def __init__(self, username = None, password = None, auto_login = True, access_token = None):
        self.auth_manager = AuthManager(username, password, access_token)
        self.notebook_manager = NotebookManager(self.auth_manager)
        if auto_login:
            self.login()

    @utils.adapter('notebook_manager')
    def ls_notebooks(self):
        pass

    @utils.adapter('auth_manager')
    def login(self, username = None, password = None):
        pass

    @property
    def is_logged(self):
        return bool(self.auth_manager.access_token.get('user_id'))

    def find_notes(self, keyword, count = 200):
        return self.notebook_manager.find_notes(keyword, count = 200)

    def get_access_token(self):
        if not self.is_logged:
            return {}

        return self.auth_manager.access_token

