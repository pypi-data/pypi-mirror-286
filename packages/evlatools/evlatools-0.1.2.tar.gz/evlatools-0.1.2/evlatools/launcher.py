#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2024/4/16 18:12
import subprocess

import pytest
from loguru import logger

try:
    import setting
except ImportError:
    from . import setting


def main(command: list = None, plugins: list = None):
    command.append(f"--alluredir={setting.ALLURE_RESULT_DIR}")
    command.append(f"--json-report-file={setting.JSON_REPORT_PATH}")
    try:
        pytest.main(args=command, plugins=plugins)
    except Exception as e:
        raise RuntimeError(f"测试用例执行失败，异常信息：{str(e)}") from e


def generate_allure_report():
    args = ["allure", "generate", setting.ALLURE_RESULT_DIR, "-o", setting.ALLURE_REPORT_DIR, "--clean"]
    try:
        res = subprocess.run(args, check=True, stdout=subprocess.PIPE, text=True, timeout=60)
        if "success" in res.stdout:
            print()
            logger.info(f"测试报告生成成功，请到 {setting.ALLURE_REPORT_DIR} 目录查看 index.html")
        else:
            print()
            logger.error(f"测试报告生成失败：{res.stdout}")
    except Exception as e:
        raise Exception(f"测试报告生成异常：{e}")

# def open_allure_server(self):
#     command = ['allure', 'open', '-h', self.allure_server_host, '-p', self.allure_server_port,
#                self.allure_report_path]
#     try:
#         subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
#         logger.info(f"测试报告服务启动成功，访问地址：http://{self.allure_server_host}:{self.allure_server_port}")
#     except Exception as e:
#         raise RuntimeError(f"打开测试报告失败，异常信息：{str(e)}") from e


if __name__ == '__main__':
    main(command=[], plugins=[])
    # from evlatools import abc

    # print(abc.add(1, 2))

