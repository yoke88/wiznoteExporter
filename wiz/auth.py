#!/usr/bin/env python
#coding:utf-8
# Author        : tuxpy
# Email         : q8886888@qq.com.com
# Last modified : 2015-11-05 13:53:48
# Filename      : auth.py
# Description   : 
from __future__ import print_function, unicode_literals
from wiz.api import api_request
from wiz import e

class AuthManager(object):
    def __new__(cls, *args, **kwargs):
        if hasattr(cls, '_instance'):
            return cls._instance

        _instance = object.__new__(cls, *args, **kwargs)
        AuthManager._instance = _instance

        return _instance

    def __init__(self, username = None, password = None, access_token = None):
        self.__username, self.__password = username, password
        self.access_token = access_token

    def login(self, username = None, password = None):
        if self.access_token:
            return
        username = username or self.__username
        password = password or self.__password

        result, error = api_request('/api/login', method = 'POST',
                data = {'user_id': username, 'password': password,
                    'token': ''})

        if error:
            raise e.WizLoginFailed(error)

        self.__login_success_after(result)

    def __login_success_after(self, login_response):
        self.access_token = {
                'token'         :       login_response['token'],
                'user_id'       :       login_response['user']['user_id'],
                'kb_guid'       :       login_response['kb_guid'],
                'cert_no'        :       login_response['cookie_str'],
                }

