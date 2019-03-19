# -*- coding:utf-8 -*-

# 蓝图的初始化工作都在此完成
# 定义蓝图

from flask import Blueprint

web = Blueprint('web', __name__)


@web.app_errorhandler(404)
def not_found(e):
    '''
    AOP 面向切面编程，对于404错误的异常，统一可以用这个方式进行处理
    特别是对于first_or_404会抛出的异常，不需要去重复编写异常处理方法
    :param e:异常处理对象
    :return:抛出自定义的页面，或者可以自己去实现对异常的处理
    '''
    return '处理错误，请联系管理员', 404


from apps.web import book
from apps.web import wish
from apps.web import main
from apps.web import gift
from apps.web import drift
from apps.web import auth