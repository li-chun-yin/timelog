# -*- coding: utf-8 -*-

def datetime_format(datetime, format_value):
    #unix 时间戳转换为指定格式的日期时间格式
    import time
    localtime   = time.localtime(int(datetime))
    formated    = time.strftime(format_value, localtime)
    return formated

def unixtime(timestamp, format_value):
    #指定格式的日期时间格式转换为unix时间戳
    import time
    mktime  = time.strptime(str(timestamp), format_value)
    return int(time.mktime(mktime))
    