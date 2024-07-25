#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2024/4/16 18:12
import subprocess
from pathlib import Path

import pytest
from loguru import logger

# 测试报告生成目录
allure_report_dir = Path.cwd().joinpath("report/allure-report")

# 测试结果生成目录
allure_result_dir = Path.cwd().joinpath("report/allure-result")


# 执行pytest方法
def pytest_main(commands=None, plugins=None):
    commands.append(f"--alluredir={allure_result_dir}")
    print(f"pytest_args: {" ".join(commands)}")
    try:
        pytest.main(args=commands, plugins=plugins)
    except Exception as e:
        raise RuntimeError(f"测试用例执行失败：{e}")


# 生成allure报告
def generate_allure_report():
    try:
        commands = ["allure", "generate", allure_result_dir, "-o", allure_report_dir, "--clean"]
        output = subprocess.run(commands, check=True, stdout=subprocess.PIPE, text=True, timeout=60)
        if "success" in output.stdout:
            logger.info(f"测试报告生成成功，查看地址：{allure_report_dir}/index.html")
        else:
            logger.error(f"测试报告生成失败：{output.stdout}")
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


def main(pytest_args=None, plugins=None, allure_report=False, allure_server=False):
    pytest_main(commands=pytest_args, plugins=plugins)

    if allure_report:
        generate_allure_report()

    if allure_server:
        pass


if __name__ == '__main__':
    pass



