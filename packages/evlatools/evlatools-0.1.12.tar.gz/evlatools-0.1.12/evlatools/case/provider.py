#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2024/4/10 19:07
import sys

try:
    from case.case import Render
    from utils.loaders import YAMLFile
except ImportError:
    from ..case.case import Render
    from ..comm.loadfile import YAMLFile


class DataProvider(object):

    def __init__(self, filepath):
        self._file = YAMLFile(filepath=filepath)

    @property
    def data(self):
        return self._file.read()

    @property
    def _globals(self):
        return self.data.get("globals")

    @property
    def _testcase(self):
        return self.data.get("testcase")

    def _iter_cases(self):
        items = []
        _globals = self._globals
        for testcase in self._testcase:
            items.append(Render(obj={
                "globals": _globals,
                "testcase": testcase
            }))
        return items

    def get_case_list(self):
        return self._iter_cases()

    def get_batch_case(self, ids):
        cases = self._iter_cases()
        if cases is None:
            raise ValueError("测试用例列表是空的！")

        items = []
        for case in cases:
            if case.cid in ids:
                items.append(case)
        return items

    def get_case_by_id(self, cid):
        cases = self._iter_cases()
        if cases is None:
            raise ValueError("测试用例列表是空的！")

        for case in cases:
            if case.cid == cid:
                return case

        raise ValueError(f"根据用例ID：'{cid}'，未找到这个测试用例！")

    def get_case_by_range(self, begin, end):
        cases = self._iter_cases()
        if cases is None:
            raise ValueError("测试用例列表是空的！")

        items = []
        for case in cases:
            cid = int(case.cid)
            if begin <= cid <= end:
                items.append(case)

        return items


