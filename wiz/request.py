#!/usr/bin/env python
#coding:utf-8
# Author        : tuxpy
# Email         : q8886888@qq.com.com
# Last modified : 2015-06-20 10:41:41
# Filename      : request.py
# Description   : from __future__ import unicode_literals
try:
    import httplib # py2
    try:
        from CStringIO import StringIO
    except ImportError:
        from StringIO import StringIO
    from urllib import quote_plus
except ImportError as e:
    from http import client as httplib # py3
    from io import StringIO


import urllib
import logging
import json
import gzip
import mimetypes
import utils


class CookieManager(object):
    def __init__(self):
        self.cookies = {}

    def set_cookie(self, set_cookie, value = None):
        if not set_cookie:
            return

        if value:
            name = set_cookie
            self.cookies[name] = value
            return


        for cookie_string in set_cookie.split(','):
            cookie_string = cookie_string.strip()
            cookie_item = cookie_string.split(';')[0].strip()
            name, value = cookie_item.split('=', 1)

            self.cookies[name.strip()] = value.strip()

    def generate_cookie(self):
        if not self.cookies:
            return None

        return [';'.join(["%s=%s" % (cookie_name,
            cookie_value) for cookie_name, cookie_value in self.cookies.items()
            ])]

cookie_manager = CookieManager()


def urlencode(data):
    params = []
    for key, value in data.items():
        if value == None:
            continue

        params.append("%s=%s" % (utils.utf8(key), 
            quote_plus(utils.utf8(value))))

    params_string = '&'.join(params)
    return params_string

def get_mime(file_name):
    return mimetypes.guess_type(file_name)[0] or 'application/octet-stream'

class Headers(dict):
    def __init__(self, headers):
        for _key, _values in headers:
            self.setdefault(_key, []).append(_values)

        super(Headers, self).__init__()

    def get_header(self, name, value = None):
        name = name.strip()
        if name not in self.keys():
            return value

        return self[name][0]

    def get_headers(self, name):
        name = name.strip()
        return self.get(name, [])

class Response(object):
    def __init__(self, response):
        self.response = response
        self.status_code = response.status
        self.reason = response.reason
        self.headers = Headers(response.getheaders())
        cookie_manager.set_cookie(self.headers.get_header('set-cookie'))
        self.raw_body = None
        self.content_type = self.headers.get_header('content-type', '')
        self.content = self.__parse_content(response)
        self.text = self.content

    def json(self):
        if 'json' in self.content_type:
            try:
                return json.loads(self.content)
            except ValueError:
                return {}

        else:
            return {}

    def __parse_content(self, response):
        """返回正文内容，结果是unicode"""
        content_encoding = self.headers.get('content-encoding', '')
        content = response.read()
        self.raw_body = content
        if content_encoding == 'gzip':
            content = self.ungzip_content(content)

        content_type = response.getheader('content-type').lower()
        if not ('json' in content_type  or 'text' in content_type):
            return content

        _parts = (content_type.split('charset=', 1) + ['utf-8'])[:2]
        charset = _parts[1]
        _pos = charset.find(';')
        if _pos != -1:
            charset = charset[:charset.find(';')]

        if charset.lower() == 'gb2312':
            charset = 'gbk'

        return content.decode(charset)

    def ungzip_content(self, content):
        _buf = StringIO(content)
        with gzip.GzipFile(mode = 'rb', fileobj = _buf) as _gzip_file:
            _content = _gzip_file.read()

        _buf.close()

        return _content

class Request(object):
    def __init__(self, method, url, headers = None, data = None, files = None, debug = False, cookies = None):
        assert url.startswith('http')
        url = utils.utf8(url)
        self.url = url
        self.method = method
        self.data = data or {}
        self.files = files
        self.body = None

        cookies = cookies or {}

        for name, value in cookies.items():
            cookie_manager.set_cookie(name, value)

        _split_url = httplib.urlsplit(url)
        self.host = _split_url.netloc
        self.uri = _split_url.path

        if _split_url.query:
            self.uri += '?' + _split_url.query

        if _split_url.scheme == 'https':
            Connection = httplib.HTTPSConnection
        else:
            Connection = httplib.HTTPConnection

        self.__conn = Connection(host = self.host)
        self.__conn.set_debuglevel(debug and logging.DEBUG or 0)

        self.headers = headers or {}
        self.generate_header(headers)

    def set_header(self, key, value):
        self.headers[utils.utf8(key)] = utils.utf8(value)

    def generate_header(self, headers = None):
        headers = headers or {}
        self.set_header('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:36.0) Gecko/20100101 Firefox/36.0)')
        self.set_header('Host', self.host)
        cookie_header = cookie_manager.generate_cookie()
        if cookie_header:
            self.set_header('Cookie', cookie_header)


        for key, value in headers.items():
            self.set_header(key, value)

    def __request(self):
        def utf8_headers(headers):
            _headers = {}
            for key, value in headers.items():
                _headers[utils.utf8(key)] = utils.utf8(value)

            return _headers

        conn = self.__conn
        conn.request(utils.utf8(self.method), utils.utf8(self.uri), body = utils.utf8(self.body),
            headers = utf8_headers(self.headers))

        response = conn.getresponse()

        return Response(response)

    def request(self):
        return self.__request()

    def post(self):
        if not self.files:
            self.body = urlencode(self.data)
            self.set_header('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
            return self.__request()
        boundary = '---------------------------14484134827975982172037180455'
        self.set_header('Content-Type', 'multipart/form-data; boundary=' + boundary)
        self.body = self.__made_multipart_data(boundary)
        return self.__request()

    def put(self):
        return self.post()

    def delete(self):
        return self.post()

    def __made_multipart_data(self, boundary):
        body = ''
        CRLF = '\r\n'
        for _name in self.files:
            _file = self.files[_name]
            if isinstance(_file, (list, tuple)):
                file_name, file_content, mime_type = (_file + ('', ''))[:3]
                mime_type = mime_type or get_mime(file_name)
            else:
                file_name = _name
                file_content = _file
                mime_type = get_mime(file_name)
            
            _body_string = '--{boundary}{CRLF}Content-Disposition: form-data; name="{name}"; filename="{filename}"{CRLF}Content-Type: {mimetype}{CRLF2}{content}{CRLF}'.format(boundary = boundary, name = _name, filename = file_name, CRLF = CRLF, mimetype = mime_type, CRLF2 = CRLF * 2, content = file_content)
            body += _body_string

        for _key, _value in self.data.items():
            _body_string = '--{boundary}{CRLF}Content-Disposition: form-data; name="{name}"{CRLF2}{content}{CRLF}'.format(boundary = boundary, name = _key, CRLF = CRLF, CRLF2 = CRLF * 2, content = _value)

            body += _body_string

        body += '--' + boundary + '--'

        return body

    def get(self):
        self.body = None
        if '?' in self.url:
            _split_char = '&'
        else:
            _split_char = '?'

        if self.data:
            self.uri += _split_char + urlencode(self.data)

        return self.__request()


def get(url, *args, **kwargs):
    request = Request('GET', url, *args, **kwargs)
    return request.get()

def post(url, *args, **kwargs):
    request = Request('POST', url, *args, **kwargs)
    return request.post()

def put(url, *args, **kwargs):
    request = Request('PUT', url, *args, **kwargs)
    return request.put()

def delete(url, *args, **kwargs):
    request = Request('DELETE', url, *args, **kwargs)

    return request.delete()


