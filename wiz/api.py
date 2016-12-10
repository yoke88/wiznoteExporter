#!/usr/bin/env python
#coding:utf-8
# Author        : tuxpy
# Email         : q8886888@qq.com.com
# Last modified : 2015-11-02 10:37:51
# Filename      : api.py
# Description   : 
from __future__ import print_function, unicode_literals
try:
    import httplib
    from urllib import quote_plus
except ImportError as e: # py3
    from http import client as httplib
    from io import StringIO
    from urllib.parse import quote_plus

from wiz import request, config, e
from functools import wraps

__all__ = ['api_request']

def downattr(path):
    url = config.host + path
    response = request.get(url)
    return response.raw_body

def api_request(path, method = 'GET', data = None, cookies = None):
    url = config.host + path
    data = data or {}
    data['api_version'] = config.version
    data['client_type'] = config.client_type
    headers = {
            'Accept'            :       'application/json, text/javascript, */*; q=0.01',
            'Accept-Language'   :       'zh-CN,en-US;q=0.7,en;q=0.3',
            }
    method = getattr(request, method.lower())
    response = method(url = url, data = data, headers = headers, 
            cookies = cookies)

    result = response.json()
    result['code'] = int(result['code'])
    error = ''
    message = result['message']
    if result['code'] != 200:
        error = message

    return result, error

