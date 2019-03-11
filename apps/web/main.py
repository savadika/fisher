# -*- coding:utf-8 -*-
from flask import render_template

from apps.apis.YuShuBook import YuShuBook
from apps.models.gift import Gift
from apps.view_models.book import BookViewModel
from . import web
from flask_login import login_required

__author__ = '七月'


# 实现首页效果，查询出所有的gift
@web.route('/')
@login_required
def index():
    recent_gifts = Gift.recent()
    books = []
    bookmodel = BookViewModel()
    yushu = YuShuBook()
    # 根据礼物去查询书籍信息，返回到首页
    for gift in recent_gifts:
        result = yushu.return_isbn(gift.isbn)
        newsresult={}
        newsresult['author'] = result['author'][0]
        newsresult['isbn'] = result['isbn']
        newsresult['image'] = result['image']
        newsresult['title'] = result['title']
        newsresult['summary'] = result['summary']
        books.append(newsresult)
    return render_template('index.html', recent=books)


@web.route('/personal')
def personal_center():
    pass
