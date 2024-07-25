#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2024/4/29 22:30
import os
import re

import yaml

from evlatools.comm import template


class YAMLFile(object):

    # 修改PyYAML的加载器，保持日期格式为字符串
    yaml.SafeLoader.yaml_implicit_resolvers = {
        k: [r for r in v if r[0] != 'tag:yaml.org,2002:timestamp']
        for k, v in yaml.SafeLoader.yaml_implicit_resolvers.items()
    }

    def __init__(self, filepath):
        if os.path.exists(path=filepath):
            self._filepath = filepath
        else:
            raise FileNotFoundError(f"[ {filepath} ] This file cannot be found!")

    @staticmethod
    def _replace(data):
        def replace_variable(match):
            variable_name = match.group(1)
            return os.getenv(variable_name, match.group(0))

        return re.sub(r'\$\{(\w+)}', replace_variable, data)

    def read(self):
        try:
            with open(file=self._filepath, mode='r', encoding='utf-8') as file:
                content = self._replace(data=file.read())
                data = yaml.safe_load(stream=content)
                return data
        except Exception as e:
            raise e

    def write(self, data, mode='w'):
        try:
            with open(file=self._filepath, mode=mode, encoding='utf-8') as file:
                yaml.dump(data=data, stream=file, default_flow_style=False, allow_unicode=True)
        except Exception as e:
            raise e

    def append(self, key, val):
        data = self.read()
        if data is None:
            data = {}

        data[key] = val
        self.write(data=data)

    def remove(self, key=None):
        if key is None:
            self.write(data=None)
        else:
            data = self.read()
            if key in data:
                del data[key]
                self.write(data=data)

    def render(self):
        return template.render(self.read())
