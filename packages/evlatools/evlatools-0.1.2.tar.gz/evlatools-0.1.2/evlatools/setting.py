#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2024/5/17 16:03
import os
from pathlib import Path


class ProjectPath:

    _rpath = Path(__file__).parent

    def __init__(self, ):
        self._proj_path = Path(__file__).parent

    @classmethod
    def join(cls, path):
        return cls._rpath / path


# 测试报告目录
ALLURE_REPORT_DIR = Path(__file__).parent / "report/allure-report"

# 测试结果目录
ALLURE_RESULT_DIR = Path(__file__).parent / "report/allure-result"

# 测试报告JSON文件
JSON_REPORT_PATH = Path(__file__).parent / "report/report.json"
