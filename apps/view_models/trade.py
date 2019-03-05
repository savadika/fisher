# -*- coding:utf-8 -*-
# 使用tradeinfo来对gift或者wish进行数据的转化
from datetime import datetime


class Tradeinfo:
    # 定义构造函数，生成所需要的数据
    def __init__(self, goods):
        self.total = 0
        self.trades = []
        self.__parse(goods)

    # 定义一组数据的转化
    def __parse(self, goods):
        self.total = len(goods)
        # 使用【列表推导式】来快速实现for循环，快速生成一个列表
        # 什么时候需要用列表推导式，当需要生成一组列表的时候
        self.trades = [self._map_to_single(single) for single in goods]

    # 定义单个数据的转化
    def _map_to_single(self, single):
        return dict(
            user_name=single.user.nickname,
            time=single.create_time[0:10],
            id=single.id
        )
