#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2024/5/29 17:54
import json

from jsonpath_ng.ext.parser import parse
from evlatools.comm.cryptolib import encrypt


def _find_by_expression(obj, expr) -> list:
    return parse(expr).find(obj)


def _find_match_value(obj, expr, index=0):
    items = []
    for match in _find_by_expression(obj, expr):
        items.append(match.value)

    if items:
        if index is None:
            return items
        else:
            return items[index]


def _find_match_node(obj, expr):
    mlist = _find_by_expression(obj, expr)
    if len(mlist) == 1:
        match = mlist[0]
    else:
        match = mlist
    return _ChildNodeHandle(obj, match)


def _find_and_replace(obj, match, action):
    def _replace_value(_match):
        _mlist = _find_by_expression(obj, expr=str(_match.full_path))
        for _m in _mlist:
            if callable(action):
                _m.full_path.update(obj, action(_m.value))
            else:
                raise ValueError("提供的参数不可调用！")

    if isinstance(match, list):
        for m in match:
            _replace_value(_match=m)
    else:
        _replace_value(match)


def _iterator_match(mlist):
    return [match.value for match in mlist]


def _append_value(match, *args):
    if isinstance(match.value, list):
        match.value.append(*args)
    else:
        raise ValueError("当前节点不支持添加元素！")


def _set_value(match, key, value):
    if isinstance(match.value, dict):
        match.value[key] = value
    else:
        raise ValueError("当前节点不支持添加键值对！")


class _Action:

    def __init__(self, obj, match):
        self._obj = obj
        self._match = match

    def set(self, key, value):
        if isinstance(self._match, list):
            for match in self._match:
                _set_value(match, key, value)
        else:
            _set_value(self._match, key, value)

    def set_property(self, key, value):
        if isinstance(self._match, list):
            for match in self._match:
                _set_value(match, key, value)
        else:
            _set_value(self._match, key, value)

    def append(self, *args):
        if isinstance(self._match, list):
            for match in self._match:
                _append_value(match, *args)
        else:
            _append_value(self._match, *args)

    def update(self, value):
        if isinstance(self._match, list):
            for match in self._match:
                match.full_path.update(self._obj, value)
        else:
            self._match.full_path.update(self._obj, value)
        return self

    def remove(self):
        if isinstance(self._match, list):
            for match in self._match:
                print(match.full_path)
        else:
            path = str(self._match.path)
            del self._match.context.value[path]

    def encrypt(self, method="aes"):
        _find_and_replace(self._obj, self._match, lambda x: encrypt(x, method))

    def add_cache(self, key):
        from evlatools.comm import cache
        if isinstance(self._match, list):
            cache.set(key, _iterator_match(self._match))
        else:
            cache.set(key, self._match.value)


class _ChildNodeHandle(_Action):

    def __init__(self, obj, match):
        super().__init__(obj, match)

    def find(self, expr):
        if isinstance(self._match, list):
            match = _iterator_match(self._match)
            return _find_match_node(match, expr)
        else:
            return _find_match_node(self._match.value, expr)

    def get(self, expr, index=0):
        if isinstance(self._match, list):
            match = _iterator_match(self._match)
            return _find_match_value(match, expr, index)
        else:
            return _find_match_value(self._match.value, expr, index)

    def read(self, expr, index=0):
        return self.get(expr, index)

    def __str__(self):
        return str(self._obj)


class JsonHandle(object):

    def __init__(self, obj):
        self._obj = obj

    def replace(self, expr, value):
        mlist = _find_by_expression(self._obj, expr)
        for match in mlist:
            match.full_path.update(self._obj, value)

    def find(self, expr):
        return _find_match_node(self._obj, expr)

    def get(self, expr, index=0):
        return _find_match_value(self._obj, expr, index)

    def read(self, expr, index=0):
        return self.get(expr, index)

    def to_dict(self):
        return self._obj

    def to_text(self, indent=None):
        return json.dumps(self._obj, ensure_ascii=False, indent=indent)

    def values(self):
        return self._obj

    def __str__(self, *args, **kwargs):
        return str(self._obj)


if __name__ == '__main__':
    json_data = {
        "method": "POST",
        "headers": {"Content-Type": "application/json;charset=UTF-8"},
        "payload": {
            "username": "lz8VUK2UCUGPu7lFATm1pg==",
            "password": "/cSUX3E93Ywyjpu1Y1AaVg==",
            "channelId": "CH57632512",
            "loginType": "aihelper",
            "showVerifyCode": True,
            "verifyCode": "",
            # "data": ["1", "2", "3", "4"]
            "data": {
                "username": "111",
                "password": ["1", "2", "3", "4"],
                "code": {
                    "aa": "11",
                    "bb": "22",
                }
            },
            "list": ["1", "2", "3", "4"]

        },
        "data": {
            "username": "222",
            "password": 123,
            "code": {
                "aa": "11",
                "bb": "22",
            },
            "list": ["1", "2", "3", "4"]
        }
    }

    case = JsonHandle(json_data)

    case.replace("username", "555")

    # case.find("$.payload").find("$.username").update("345").encrypt()
    #
    # data = case.find("$..data")
    #
    # data.find("$..username").update("345").encrypt()
    #
    # case.find("$.data").find("$.list").append({"pla": "22"})
    #
    # case.find("$.data").find("$.code").set("dd", "33")
    #
    # print(case.find("$..data").get("$..username"))
    #
    # print(case.find("$.data").get("$.username"))
    #
    # print(case.find("$.method").remove())

    print(case.to_text(indent=4))
