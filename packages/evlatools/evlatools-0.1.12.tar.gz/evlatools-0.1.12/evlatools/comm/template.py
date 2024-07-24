#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2023/8/27 16:53
import json

import jinja2
import yaml
import re

from evlatools.comm import mock, cache, dateutil
from evlatools.comm.cryptolib import encrypt


# 模板函数
builtin = dict()
builtin["mock"] = mock
builtin["cache"] = cache
builtin["encrypt"] = encrypt
builtin["dateutil"] = dateutil


def to_string(value):
    return f'"{value}"'


# 模板过滤器
filters = dict()
filters["str"] = to_string
filters["encrypt"] = encrypt


def render(obj, *args, **kwargs):
    tmpl = RenderTemplate()
    if isinstance(obj, str):
        output = tmpl.render_template_string(obj, *args, **kwargs)
    elif isinstance(obj, dict):
        output = tmpl.render_template_object(obj, *args, **kwargs)
    elif isinstance(obj, list):
        output = tmpl.render_template_array(obj, *args, **kwargs)
    else:
        raise Exception(f"‘{obj}’ 是不支持的渲染类型！")
    return output


class RenderTemplate(object):

    def __init__(self):
        # 初始化模板引擎
        self._env = jinja2.Environment()
        self._env.variable_start_string = "${"
        self._env.variable_end_string = "}"

        # 初始化过滤器
        self._env.filters.update(filters)

    def render_template_array(self, array, *args, **kwargs):
        """
        传入list对象，通过模板字符串递归查找模板字符串
        :param array:
        :param args:
        :param kwargs:
        :return:
        """
        if isinstance(array, list):
            items = []
            for arr in array:
                if isinstance(arr, str):
                    items.append(self.render_template_string(arr, *args, **kwargs))
                elif isinstance(arr, list):
                    items.append(self.render_template_array(arr, *args, **kwargs))
                elif isinstance(arr, dict):
                    items.append(self.render_template_object(arr, *args, **kwargs))
                else:
                    items.append(arr)
            return items
        else:
            return array

    def render_template_object(self, obj: dict, *args, **kwargs):
        """
        传入dict对象，通过模板字符串递归查找模板字符串，转行成新的数据
        :param obj:
        :param args:
        :param kwargs:
        :return:
        """
        if isinstance(obj, dict):
            for key, value in obj.items():
                if isinstance(value, str):
                    obj[key] = self.render_template_string(value, *args, **kwargs)
                elif isinstance(value, dict):
                    self.render_template_object(value, *args, **kwargs)
                elif isinstance(value, list):
                    obj[key] = self.render_template_array(value, *args, **kwargs)
                else:
                    pass
        return obj

    def render_template_string(self, ts, *args, **kwargs):
        """
        渲染模板字符串, 改写了默认的引用变量语法 {{var}}, 换成 ${var}.
        在模板中引用变量语法：${var}.
        在模板中调用函数语法：${fun()}.
        :param ts: template str，模板字符串
        :param args:
        :param kwargs:
        :return: 渲染之后的值
        """

        def rrts(match) -> str:
            """
            渲染模板时加载内部引用变量
            :param match:
            :return:
            """
            groups = match.group()
            result = str(groups).lstrip("${").rstrip("}")
            if "${" in result and "}" in result and result.find("${") < result.find("}"):
                _fs = self._env.from_string(result)
                _tr = _fs.render(*args, **kwargs)
                # _tr = _fs.render(self.builtins)

                return "${" + _tr + "}"
            else:
                return groups

        # 正则替换
        ts = re.sub(r"\$\{(.+?)\}", rrts, ts)
        fs = self._env.from_string(ts)
        # tr = fs.render(*args, **kwargs)
        tr = fs.render(builtin, *args, **kwargs)

        if ts.startswith("${") and ts.endswith("}") and ts.count("${") == 1:
            trs = ts.rstrip("}").lstrip("${")
            if kwargs.get(trs):
                return kwargs.get(trs)

            # 内置函数str()
            if trs.startswith("str(") and trs.endswith(")"):
                return str(tr)

            if trs.startswith("dumps(") and trs.endswith(")"):
                return json.dumps(tr)

            if trs.startswith("loads(") and trs.endswith(")"):
                return json.loads(tr)

            try:
                content = yaml.safe_load(tr)
                return content
            except Exception as msg:  # noqa
                return tr

        else:
            return tr
