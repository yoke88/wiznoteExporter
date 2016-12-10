#!/usr/bin/env python
#coding:utf-8
# Author        : tuxpy
# Email         : q8886888@qq.com.com
# Last modified : 2015-11-02 10:53:15
# Filename      : e.py
# Description   : 
from __future__ import print_function, unicode_literals
import sys

class WizException(Exception):
    def __init__(self, reason):
        self.reason = reason
        Exception.__init__(self, reason)
        sys.stderr.write(reason + '\n')

class WizLoginFailed(WizException):
    pass

class WizTokenInvalid(WizException):
    pass


