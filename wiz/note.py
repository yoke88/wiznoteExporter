#!/usr/bin/env python
#coding:utf-8
# Author        : tuxpy
# Email         : q8886888@qq.com.com
# Last modified : 2015-11-05 17:10:26
# Filename      : note.py
# Description   : 
from __future__ import print_function, unicode_literals
from wiz import api
from wiz.utils import ObjectDict, cache_self, ZipFile
import os
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

class NoteData(ObjectDict):
    pass

class Note(ObjectDict):
    @property
    @cache_self
    def data(self):
        return self._manager.get_note_data(self.guid)

class _AttrData(object):
    def __init__(self, url, name = None):
        self.url = url
        self.name = name or os.path.basename(url)

    @property
    @cache_self
    def data(self):
        return api.downattr(self.url)

class NoteImageData(_AttrData):
    pass

class NoteAttrData(_AttrData):
    @property
    @cache_self
    def data(self):
        _zip_data = super(NoteAttrData, self).data
        _zip_io = StringIO(_zip_data)
        with ZipFile(_zip_io) as _zip_instance:
            return _zip_instance.read(_zip_instance.namelist()[0])

