# -*- coding: utf-8 -*-#

# -------------------------------------------------------------------------------
# Name:         my_time
# Description:  个人时间库
# Author:       ylf
# Date:         2019-03-31
# -------------------------------------------------------------------------------

from datetime import datetime, date
import time

def timestamp_to_time(timestamp):
    """定义时间戳转化为正常时间"""
    datetimeArray = date.fromtimestamp(int(float(timestamp)))
    str_time = datetimeArray.strftime('%Y-%m-%d')
    return str_time
