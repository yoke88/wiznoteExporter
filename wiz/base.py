#!/usr/bin/env python
#coding:utf-8
# Author        : tuxpy
# Email         : q8886888@qq.com.com
# Last modified : 2015-11-05 13:58:25
# Filename      : base.py
# Description   : 
from __future__ import unicode_literals, print_function

from wiz import e
from wiz.api import api_request

__all__ = ['BaseManager']

class BaseManager(object):
    def __init__(self, auth_manager):
        self._auth_manager = auth_manager

    def api_request(self, path, method = 'GET', data = None, auto_raise = True):
        data = data or {}
        data.update(self._auth_manager.access_token)

        cert_no = data.pop('cert_no')
        wiz_id = data.get('user_id')
        token = data.get('token')
        if cert_no and wiz_id and token:
            cookies = {
                        'CertNo'    :   cert_no,
                        'WizID'     :   wiz_id,
                        'token'     :   token,
                    }
        else:
            cookies = {}

        result, error = api_request(path, method, data, 
                cookies)
        if error and auto_raise:
            if result['code'] == 301:
                raise e.WizTokenInvalid(error)
            else:
                raise e.WizException(error)

        return result, error


