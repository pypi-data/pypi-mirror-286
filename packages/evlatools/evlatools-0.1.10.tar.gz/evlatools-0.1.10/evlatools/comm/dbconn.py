#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2024/1/14 19:28
import json
from warnings import filterwarnings

import pymysql
import redis


class MysqlClient(object):

    # 忽略mysql告警信息
    filterwarnings("ignore", category=pymysql.Warning)

    def __init__(self, host, port, username, password, dbname=None):
        self._conn = pymysql.connect(host=host, port=port, user=username, password=password, db=dbname)
        self._curs = self._conn.cursor()

    def __del__(self):
        self._curs.close()  # 关闭游标
        self._conn.close()  # 关闭数据库

    def query(self, sql, state="all"):
        """
        查询
        :param sql:
        :param state:
        :return:
        """
        try:
            # 查询数据库，sql输入查询的语句
            self._curs.execute(sql)
            if state == "all":
                # 查询全部
                data = self._curs.fetchall()
            else:
                # 单条查询
                data = self._curs.fetchone()
            return data
        except Exception as e:
            print(f"数据库查询异常：{e}")

    def execute(self, sql):
        """
        更新、删除、新增
        :param sql:
        :return:
        """
        try:
            # 操作数据库，sql输入更新、删除、新增的语句
            rows = self._curs.execute(sql)
            # 提交事务
            self._conn.commit()
            return rows
        except Exception as e:
            print(f"数据库操作异常：{e}")
            # 不成功的话就撤销数据 conn.rollback()
            self._conn.rollback()


class RedisClient(object):

    def __init__(self, host, port, password, db=0):
        try:
            self._redis = redis.StrictRedis(host=host, port=port, password=password, db=db, decode_responses=True)
        except redis.exceptions.ConnectionError as e:
            raise redis.exceptions.ConnectionError("redis连接失败，错误信息：{}".format(e))
        except Exception as e:
            raise redis.RedisError("未知错误：{}".format(e))

    def set(self, name, value):
        self._redis.set(name, value)

    def get(self, name):
        return self._redis.get(name)

    def keys(self):
        return self._redis.keys()

    def clear(self):
        self._redis.flushdb()
