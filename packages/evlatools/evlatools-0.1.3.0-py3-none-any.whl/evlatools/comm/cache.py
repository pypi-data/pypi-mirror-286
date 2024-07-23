#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2024/6/23 13:12
import time

from cacheout import Cache

try:
    from jsonpath import JsonHandle
except ImportError:
    from .jsonpath import JsonHandle


class _Cache(Cache, JsonHandle):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def data(self):
        return dict(self.items())

    def read(self, expr):
        data = self.data()
        return JsonHandle(data).read(expr)


cache = _Cache()


