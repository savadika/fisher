# -*- coding:utf-8 -*-

# 蓝图的初始化工作都在此完成
# 定义蓝图
from flask import Blueprint

web = Blueprint('web', __name__)

from apps.web import book
from apps.web import auth
from apps.web import drift
from apps.web import gift
from apps.web import main
from apps.web import wish