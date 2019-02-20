from flask import current_app, flash, render_template, url_for, redirect
from apps import db
from apps.models.gift import Gift
from apps.models.user import User
from . import web
from flask_login import login_required, current_user
__author__ = 'ylf'


@web.route('/my/gifts')
@login_required  # 要使用这个，必须在user模型中定义方法
def my_gifts():
    return '111'


#  赠送图书视图函数
@web.route('/gifts/book/<isbn>')
@login_required
def save_to_gifts(isbn):
    # 如何快速导入类：光标在这个类上，然后按alt+enter
    with db.auto_commit():
        gift = Gift()
        gift.isbn = isbn
        gift.uid = current_user.id  # current_user 实际上就是通过模型返回的USER类，里面有一个id
        # 此处可以直接操作关联的user模型
        print(current_user)
        current_user.beans += current_app.config['BEANS_UPLOAD_ONE_BOOK']
        db.session.add(gift)  # 使用db.session来进行数据库的提交操作
    return '111'


@web.route('/gifts/<gid>/redraw')
def redraw_from_gifts(gid):
    pass


# 查询一个礼物的所有者
@web.route('/gift/test1')
def gift_test_single():
    gift = Gift.query.filter_by(id=3).first()
    return gift.user.nickname

# 查询一个人的所有礼物
@web.route('/gift/test2')
def gift_test_multiple():
    user = User.query.filter_by(id=17).first()
    gifts = user.gift
    for gift in gifts:
        return gift.isbn
