#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2024/6/23 13:12
import time

from cacheout import Cache


class CacheUtils(Cache):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def content(self):
        return dict(self.items())

    def read(self, expr):
        from evlatools.comm.jsonpath import JsonHandle
        return JsonHandle(self.content).read(expr)




