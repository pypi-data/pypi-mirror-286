#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2024/4/10 19:06
import json
import re

import allure
import pytest
from loguru import logger

from evlatools.client import httpclient
from evlatools.comm import template
from evlatools.comm.jsonpath import JsonHandle
from evlatools.comm.validator import Assert


class Case(JsonHandle):

    def __init__(self, case):
        super().__init__(obj=case)

    @property
    def cid(self):
        return self.get(expr="$.id")

    @property
    def skip(self):
        return self.get(expr="$.skip")

    @property
    def epic(self):
        return self.get(expr="$.epic")

    @property
    def feature(self):
        return self.get(expr="$.feature")

    @property
    def story(self):
        return self.get(expr="$.story")

    @property
    def title(self):
        return self.get(expr="$.title")

    @property
    def level(self):
        return self.get(expr="$.level")

    @property
    def extract(self):
        return self.get(expr="$.extract")

    @property
    def validate(self):
        return self.get(expr="$.validate")

    @property
    def request(self):
        class _Request(JsonHandle):
            def __init__(self, obj: dict):
                super().__init__(obj=obj)

            @property
            def url(self) -> str:
                return self.get(expr="$.url")

            @property
            def method(self) -> str:
                return self.get(expr="$.method")

            @property
            def headers(self):
                rest = self.get(expr="$.headers")
                return JsonHandle(obj=rest)

            @property
            def cookies(self):
                rest = self.get(expr="$.cookies")
                return JsonHandle(obj=rest)

            @property
            def payload(self):
                rest = self.get(expr="$.payload")
                return JsonHandle(obj=rest)

        request = self.get("$.request")
        return _Request(obj=request)

    def execute(self, title=None):
        if self.skip:
            pytest.skip(reason=f"当前用例 ‘{self.cid}’ 已被标记为不执行！")

        else:
            title = title if title else self.title

            try:
                # 请求内容
                url = self.request.url
                method = self.request.method
                headers = self.request.headers.to_dict()
                cookies = self.request.cookies.to_dict()
                payload = self.request.payload.to_dict()
                logger.info(f"发送请求 >>>>> {title} | {method.center(4)} | {self.request.to_text()}")

                # 发送请求
                response = httpclient.request(url=url,
                                              method=method,
                                              headers=headers,
                                              cookies=cookies,
                                              payload=payload
                                              ).execute()

            except Exception as e:
                logger.exception(f"请求发送异常：{e}")
                raise

            # 判断响应状态码，200表示成功，其他失败
            status_code = response.status_code
            if status_code == 200:
                output = ""
                content_type = response.headers.get("Content-Type")
                if content_type is None:
                    logger.info(f"接收响应 <<<<< {title} | {str(status_code).center(4)} | {response.headers.to_text()}")

                elif "event-stream" in content_type:
                    lines = response.iter_lines()
                    for line in lines:
                        if line:
                            # 处理每行响应数据
                            data = line.decode('utf-8')
                            match = re.search(r"data:(.*)", data)
                            if match:
                                output += match.group(1)
                    logger.info(f"接收响应 <<<<< {title} | {str(status_code).center(4)} | {output}")

                else:
                    logger.info(f"接收响应 <<<<< {title} | {str(status_code).center(4)} | {response.to_text()}")

                # 添加allure属性
                allure.dynamic.epic(self.epic)
                allure.dynamic.feature(self.feature)
                allure.dynamic.story(self.story)
                allure.dynamic.title(self.title)
                allure.dynamic.severity(self.level)

                # 请求参数添加到allure附件
                attach_body = response.request.to_text()
                attach_type = allure.attachment_type.JSON
                allure.attach("请求参数", attach_body, attach_type)

                # 响应参数添加到allure附件
                content_type = response.headers.get("Content-Type")
                if content_type is None:
                    attach_body = response.status_code
                    attach_type = allure.attachment_type.TEXT
                elif not content_type:
                    attach_body = response.status_code
                    attach_type = allure.attachment_type.TEXT
                elif "application/json" in content_type:
                    attach_body = response.content.to_text()
                    attach_type = allure.attachment_type.JSON
                elif "event-stream" in content_type:
                    attach_body = response.inst.text
                    attach_type = allure.attachment_type.TEXT
                elif "image" in content_type:
                    attach_body = response.byte
                    attach_type = allure.attachment_type.PNG
                else:
                    attach_body = response.byte.decode("utf-8")
                    attach_type = allure.attachment_type.TEXT
                allure.attach("响应参数", attach_body, attach_type)

                if self.validate:
                    # 遍历所有验证项，并断言结果
                    for val in self.validate:
                        # key是断言方法，value是断言数据
                        for key, value in val.items():
                            method = value[0]  # 验证项
                            expres = value[1]  # 表达式
                            expect = value[2]  # 预期值
                            if method.lower() == "status":
                                actual = response.status_code
                                Assert.check(key, actual, expect)
                            elif method.lower() == "content":
                                actual = response.content.get(expres)
                                Assert.check(key, actual, expect)
                            else:
                                raise ValueError(f"‘{method}’ 暂不支持断言!")

                if self.extract:
                    # 遍历所有提取项，并缓存数据
                    for ext in self.extract:
                        # key是提取项，value是提取数据
                        for key, value in ext.items():
                            method = value[0]  # 缓存名
                            expres = value[1]  # 表达式
                            if key.lower() == "cookies":
                                response.cookies.find(expres).add_cache(method)
                            elif key.lower() == "content":
                                response.headers.find(expres).add_cache(method)
                            else:
                                raise ValueError(f"‘{method}’ 暂不支持提取!")

            else:
                logger.error(f"接收响应 <<<<< {title} | {str(status_code).center(4)} | {response.elapsed}s")

            return response

    def build(self, url=None, method=None, *args, **kwargs):
        if url is not None:
            url = self.request.url

        if method is not None:
            method = self.request.method

        return httpclient.request(url=url, method=method, *args, **kwargs)

    def __str__(self):
        return json.dumps(self._obj, ensure_ascii=False)


class Render(Case):

    def __init__(self, obj: dict):
        self._globals = obj.get("globals")
        self._testcase = obj.get("testcase")
        super().__init__(case=self._testcase)

    def render(self):
        # 更新模板函数
        context = dict()
        context.update(template.builtin)

        # 渲染全局节点
        output = template.render(self._globals, **context)

        # 更新模板函数
        context.update(output)

        # 渲染用例节点
        output = template.render(self._testcase, **context)
        return Case(case=output)


