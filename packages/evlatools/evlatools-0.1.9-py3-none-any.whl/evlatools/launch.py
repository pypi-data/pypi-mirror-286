#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2024/4/16 18:12
import os
import subprocess

import pytest
from loguru import logger


# 测试报告生成目录
allure_report_dir = os.path.join(os.getcwd(), "report/allure-report")

# 测试结果生成目录
allure_result_dir = os.path.join(os.getcwd(), "report/allure-result")


def main(commands: list = None, plugins: list = None):
    if commands is None:
        commands = []
    else:
        commands.append(f"--alluredir={allure_result_dir}")

    try:
        pytest.main(args=commands, plugins=plugins)
    except Exception as e:
        raise RuntimeError(f"测试用例执行失败，异常信息：{str(e)}") from e


def generate_report():
    args = ["allure", "generate", allure_result_dir, "-o", allure_report_dir, "--clean"]
    try:
        res = subprocess.run(args, check=True, stdout=subprocess.PIPE, text=True, timeout=60)
        if "success" in res.stdout:
            logger.info(f"测试报告生成成功，保存路径：{allure_report_dir}")
        else:
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
    main(commands=[], plugins=[])
    # generate_allure_report()


