#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2024/4/10 16:56
import json
import mimetypes
import os

import requests
from loguru import logger
from requests import exceptions
from requests.structures import CaseInsensitiveDict
from requests_toolbelt import MultipartEncoder

from evlatools.client.media import ContentTypes
from evlatools.comm.jsonpath import JsonHandle


def open_file(filepath):
    filename = os.path.basename(filepath)
    mimetype, _ = mimetypes.guess_type(filename)
    if mimetype is None:
        mimetype = "application/octet-stream"

    filedata = (filename, open(filepath, "rb"), mimetype)
    return filedata


def post(url, method="POST", payload=None, **kwargs):
    return request(url=url, method=method, payload=payload, **kwargs).execute()


def get(url, method="GET", payload=None, **kwargs):
    return request(url=url, method=method, payload=payload, **kwargs).execute()


def request(url, method, payload=None, **kwargs):
    return HTTPRequest(url=url, method=method, payload=payload, **kwargs)


class HTTPRequest(object):

    def __init__(self, url, method, payload=None, **kwargs):
        self.url = url
        self.method = method
        self.payload = payload
        self.kwagrs = kwargs

    def execute(self):
        try:
            headers = self.kwagrs.get("headers")
            # headers = CaseInsensitiveDict(headers)
            if headers is None:
                response = requests.request(url=self.url, method=self.method, params=self.payload, **self.kwagrs)

            else:
                content_type = headers.get("Content-Type")
                if content_type is None:
                    response = requests.request(url=self.url, method=self.method, params=self.payload, **self.kwagrs)

                elif content_type in ContentTypes.APPLICATION_JSON:
                    response = requests.request(url=self.url, method=self.method, json=self.payload, **self.kwagrs)

                elif content_type == ContentTypes.APPLICATION_FORM_URLENCODED:
                    response = requests.request(url=self.url, method=self.method, data=self.payload, **self.kwagrs)

                elif content_type in ContentTypes.MULTIPART_FORM_DATA:
                    for key, value in self.payload.items():
                        if not isinstance(value, str):
                            self.payload[key] = str(value)

                        if key == "file":
                            self.payload["file"] = open_file(filepath=value)

                        elif key == "files":
                            if isinstance(value, str):
                                self.payload["files"] = open_file(filepath=value)

                            elif isinstance(value, list):
                                for i, file in enumerate(value):
                                    filedata = open_file(filepath=file)
                                    if len(value) == 1:
                                        self.payload["files"] = filedata
                                    else:
                                        self.payload[f"files{i}"] = filedata

                            else:
                                raise TypeError("请输入正确的文件路径！")

                    print(f"上传文件请求参数：{self.payload}")
                    encoder = MultipartEncoder(fields=self.payload)
                    headers["Content-Type"] = encoder.content_type

                    response = requests.request(url=self.url, method=self.method, data=encoder, **self.kwagrs)

                else:
                    raise TypeError(f"暂不支持 {content_type} 类型！")

        except exceptions.RequestException as e:
            raise exceptions.RequestException(f"请求失败，异常信息：{e}")
        except Exception as e:
            raise Exception(f"请求失败，未知错误：{e}")

        return HTTPResponse(response=response)


class HTTPResponse(object):

    def __init__(self, response: requests.Response):
        self._response = response

    @property
    def inst(self):
        return self._response

    def to_dict(self, *args, **kwargs):
        return self._response.json(*args, **kwargs)

    def to_text(self, **kwargs):
        content_type = self._response.headers.get("content-type")
        if content_type:
            if content_type in ContentTypes.APPLICATION_JSON:
                return json.dumps(self.to_dict(), ensure_ascii=False, **kwargs)
            else:
                return None
        return None

    def raise_for_status(self):
        return self._response.raise_for_status()

    def iter_lines(self):
        return self._response.iter_lines()

    @property
    def byte(self):
        return self._response.content

    @property
    def content(self):
        content = self._response.json()
        return JsonHandle(obj=content)

    @property
    def cookies(self):
        cookies = self._response.cookies.get_dict()
        return JsonHandle(obj=cookies)

    @property
    def headers(self):
        headers = self._response.headers
        return JsonHandle(obj=dict(headers))

    @property
    def status_code(self):
        return self._response.status_code

    @property
    def elapsed(self):
        return self._response.elapsed.total_seconds()

    @property
    def request(self):
        class Request(object):
            def __init__(self, response):
                self._request = response.request

            @property
            def url(self):
                return self._request.url

            @property
            def method(self):
                return self._request.method

            @property
            def headers(self):
                return self._request.headers

            @property
            def payload(self):
                return self._request.body

            def to_dict(self):
                items = dict()
                items["url"] = self.url
                items["method"] = self.method

                content_type = self.headers.get("Content-Type")
                if content_type:
                    if content_type in ContentTypes.APPLICATION_JSON:
                        body = self._request.body
                        if body:
                            items["payload"] = json.loads(body.decode(encoding="utf-8"))
                        else:
                            items["payload"] = None
                    else:
                        items["payload"] = None

                items["headers"] = dict(self.headers)
                return items

            def to_text(self, indent=None):
                return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)

        return Request(response=self._response)
