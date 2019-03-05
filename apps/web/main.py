# -*- coding:utf-8 -*-
from . import web
from flask_login import login_required

__author__ = '七月'


# 实现首页效果，查询出所有的gift
@web.route('/')
@login_required
def index():
    return '您已经成功登陆!'


@web.route('/personal')
def personal_center():
    pass
