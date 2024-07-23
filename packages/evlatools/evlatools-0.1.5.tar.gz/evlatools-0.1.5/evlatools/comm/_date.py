#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2023/11/2 16:06
import calendar
import datetime


class _Format(object):
    DATE_FORMAT = "%Y-%m-%d"
    TIME_FORMAT = "%H:%M:%S"
    DATE_TIME_FORMAT = DATE_FORMAT + " " + TIME_FORMAT

    CHN_DATE_FORMAT = "%Y年%m月%d日"
    CHN_TIME_FORMAT = "%H时%M分%S秒"
    CHN_DATE_TIME_FORMAT = CHN_DATE_FORMAT + " " + CHN_TIME_FORMAT


class DateUtils(object):

    def __init__(self):
        self._datetime = datetime

    def now(self):
        return self._datetime.datetime.now()

    def datetime(self, fmt):
        now = self._datetime.datetime.now()
        return now.strftime(fmt)

    @staticmethod
    def month_first_date(year, month):
        """
        获取指定月份的第一天日期
        :param year: 年份
        :param month: 月份
        :return: 第一天日期
        """
        return datetime.date(year, month, 1)

    @staticmethod
    def month_last_date(year, month):
        """
        获取指定月份的最后一天日期
        :param year: 年份
        :param month: 月份
        :return: 最后一天日期
        """
        return datetime.date(year, month, calendar.monthrange(year, month)[1])

    @staticmethod
    def date_of_recent_months(month=-3):
        """
        获取近几月的每一天，包含本月
        :param month:
        :return:
        """
        datenow = datetime.datetime.now()
        month_first_day = datenow.replace(day=1, month=datenow.month - abs(month))
        month_last_day = datenow.replace(day=1, month=datenow.month + 1) - datetime.timedelta(days=1)

        datelist = []
        date = month_first_day
        while date <= month_last_day:
            datelist.append(date)
            date += datetime.timedelta(days=1)

        return [date.strftime(_Format.DATE_FORMAT) for date in datelist]

    @staticmethod
    def date_of_recent_weeks(week=-0):
        """
        获取近几周的每一天，包含本周
        :param week:
        :return:
        """
        datenow = datetime.datetime.now()
        this_week_first_day = datenow - datetime.timedelta(days=datenow.weekday())
        last_week_first_day = this_week_first_day - datetime.timedelta(days=abs(week*7))

        datelist = []
        date = last_week_first_day
        while date <= this_week_first_day + datetime.timedelta(days=6):
            datelist.append(date)
            date += datetime.timedelta(days=1)

        return [date.strftime(_Format.DATE_FORMAT) for date in datelist]

    @staticmethod
    def date_of_recent_days(day=-7):
        """
        获取近几天的每一天，包含当天
        :param day:
        :return:
        """
        date_now = datetime.datetime.now()
        # 获取近7天的日期范围
        datelist = []
        for i in range(abs(day)):
            date = date_now - datetime.timedelta(days=i)
            fmt_date = date.strftime(_Format.DATE_FORMAT)

            datelist.append(fmt_date)
        return datelist

    def recent_datetime(self, timedelta, fmt, _type="days"):
        datelist = []
        for i in range(abs(timedelta)):
            ret = None
            if _type == "weeks":
                ret = self.now() - self._datetime.timedelta(weeks=i)
            elif _type == "days":
                ret = self.now() - self._datetime.timedelta(days=i)
            elif _type == "hours":
                ret = self.now() - self._datetime.timedelta(hours=i)
            elif _type == "minutes":
                ret = self.now() - self._datetime.timedelta(minutes=i)
            elif _type == "seconds":
                ret = self.now() - self._datetime.timedelta(seconds=i)

            if fmt:
                sft = ret.strftime(fmt)
            else:
                sft = ret.strftime("%Y-%m-%d")
            datelist.append(sft)
        return list(reversed(datelist))

    def recent_months(self, months, fmt):
        datenow = self.now()
        month_first_day = datenow.replace(day=1, month=datenow.month - abs(months))
        month_last_day = datenow.replace(day=1, month=datenow.month + 1) - datetime.timedelta(days=1)

        datelist = []
        date = month_first_day
        while date <= month_last_day:
            datelist.append(date)
            date += datetime.timedelta(days=1)

        newdates = []
        for date in datelist:
            if fmt:
                date = date.strftime(fmt)
            else:
                date = date.strftime("%Y-%m-%d")
            newdates.append(date)
        return newdates

    def recent_weeks(self, weeks, fmt=None):
        datenow = self.now()
        this_week_first_day = datenow - datetime.timedelta(days=datenow.weekday())
        last_week_first_day = this_week_first_day - datetime.timedelta(days=abs(weeks*7))

        datelist = []
        date = last_week_first_day
        while date <= this_week_first_day + datetime.timedelta(days=6):
            datelist.append(date)
            date += datetime.timedelta(days=1)

        newdates = []
        for date in datelist:
            if fmt:
                date = date.strftime(fmt)
            else:
                date = date.strftime("%Y-%m-%d")
            newdates.append(date)
        return newdates

    def recent_days(self, days, fmt=None):
        return self.recent_datetime(timedelta=days, fmt=fmt, _type="days")

    def recent_hours(self, hours, fmt=None):
        return self.recent_datetime(timedelta=hours, fmt=fmt, _type="hours")

    def recent_minutes(self, minutes, fmt=None):
        return self.recent_datetime(timedelta=minutes, fmt=fmt, _type="minutes")

    def recent_seconds(self, seconds, fmt=None):
        return self.recent_datetime(timedelta=seconds, fmt=fmt, _type="seconds")


