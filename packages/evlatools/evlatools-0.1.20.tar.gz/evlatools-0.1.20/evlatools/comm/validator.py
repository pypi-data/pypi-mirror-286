#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/3/5 17:24
# @File    : validator.py
# @Author  : Gao
import re


class Assert(object):

    @staticmethod
    def not_none(actual):
        assert actual is not None

    @staticmethod
    def is_none(actual):
        assert actual is None

    @staticmethod
    def equals(actual, expect):
        """
        判断实际结果和预期结果相等
        :param actual:
        :param expect:
        :return:
        """
        assert actual == expect

    @staticmethod
    def less_than(actual, expect):
        assert actual < expect

    @staticmethod
    def less_than_or_equals(actual, expect):
        assert actual <= expect

    @staticmethod
    def greater_than(actual, expect):
        assert actual > expect

    @staticmethod
    def greater_than_or_equals(actual, expect):
        assert actual >= expect

    @staticmethod
    def not_equals(actual, expect):
        assert actual != expect

    @staticmethod
    def string_equals(actual, expect):
        assert str(actual) == str(expect)

    @staticmethod
    def length_equals(actual, expect):
        print(f"实际：{actual}, 预期：{expect}")
        # expect_len = Assert._cast_to_int(expect)
        assert len(actual) == expect

    @staticmethod
    def length_greater_than(actual, expect):
        expect_len = Assert._cast_to_int(expect)
        assert len(actual) > expect_len

    @staticmethod
    def length_greater_than_or_equals(actual, expect):
        expect_len = Assert._cast_to_int(expect)
        assert len(actual) >= expect_len

    @staticmethod
    def length_less_than(actual, expect):
        expect_len = Assert._cast_to_int(expect)
        assert len(actual) < expect_len

    @staticmethod
    def length_less_than_or_equals(actual, expect):
        expect_len = Assert._cast_to_int(expect)
        assert len(actual) <= expect_len

    @staticmethod
    def contains(actual, expect):
        assert isinstance(actual, (list, tuple, dict, str))
        assert expect in actual

    @staticmethod
    def contained_by(actual, expect):
        assert isinstance(expect, (list, tuple, dict, str))
        assert actual in expect

    @staticmethod
    def regex_match(actual, expect):
        assert isinstance(expect, str)
        assert isinstance(actual, str)
        assert re.match(expect, actual)

    @staticmethod
    def startswith(actual, expect):
        assert str(actual).startswith(str(expect))

    @staticmethod
    def endswith(actual, expect):
        assert str(actual).endswith(str(expect))

    @staticmethod
    def _cast_to_int(expect):
        try:
            return int(expect)
        except Exception:
            raise AssertionError(f"%{expect} can't cast to int")

    @staticmethod
    def check(check_type, actual, expect):
        if check_type in ["=="]:
            Assert.equals(actual, expect)
        if check_type in ["eq", "equals", "equal"]:
            Assert.equals(actual, expect)
        elif check_type in ["lt", "less_than"]:
            Assert.less_than(actual, expect)
        elif check_type in ["le", "less_or_equals"]:
            Assert.less_than_or_equals(actual, expect)
        elif check_type in ["gt", "greater_than"]:
            Assert.greater_than(actual, expect)
        elif check_type in ["ge", "greater_than_or_equals", "greater_or_equals"]:
            Assert.greater_than_or_equals(actual, expect)
        elif check_type in ["ne", "not_equal"]:
            Assert.not_equals(actual, expect)
        elif check_type in ["se", "string_equals"]:
            Assert.string_equals(actual, expect)
        elif check_type in ["lq", "length_equal"]:
            Assert.length_equals(actual, expect)
        elif check_type in ["lgt", "length_greater_than"]:
            Assert.length_greater_than(actual, expect)
        elif check_type in ["lge", "length_greater_or_equals"]:
            Assert.length_greater_than_or_equals(actual, expect)
        elif check_type in ["llt", "length_less_than"]:
            Assert.length_less_than(actual, expect)
        elif check_type in ["lle", "length_less_or_equals"]:
            Assert.length_less_than_or_equals(actual, expect)
        elif check_type in ["cot", "contains"]:
            Assert.contains(actual, expect)
        else:
            if hasattr(Assert, check_type):
                getattr(Assert, check_type)(actual, expect)
            else:
                print("{} not valid check type".format(check_type))
