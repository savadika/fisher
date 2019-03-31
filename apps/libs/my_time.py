# -*- coding: utf-8 -*-#

#-------------------------------------------------------------------------------
# Name:         my_time
# Description:  个人时间库
# Author:       ylf
# Date:         2019-03-31
#-------------------------------------------------------------------------------

import time

def timestamp_to_time(timestamp):
    """定义时间戳转化为正常时间"""
    time_str = time.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
    ss = str(time.mktime(time_str))
    dt = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(float(ss)))
    return dt