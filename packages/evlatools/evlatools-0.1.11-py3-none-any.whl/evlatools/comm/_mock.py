#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2024/6/23 13:24
import uuid

from faker import Faker


class MockUtils(Faker):

    def __init__(self, locale='zh_CN'):
        super().__init__(locale=locale)

    @staticmethod
    def uuid():
        return uuid.uuid4()

    def randtext(self, text, a=1000, b=9999):
        return f"{text}{self.random.randint(a, b)}"

