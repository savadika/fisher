from flask import current_app, flash, render_template, url_for, redirect
from apps import db
from apps.models.gift import Gift
from apps.models.user import User
from apps.models.wish import Wish
from apps.view_models.gift import GiftViewModel
from . import web
from flask_login import login_required, current_user
from datetime import datetime
__author__ = 'ylf'


@web.route('/my/gifts')
@login_required
def my_gifts():
    '''
    :return: 返回我的所有礼物，以及对应的wish的清单
    '''
    my_gift_list = Gift.gift_of_mine()
    my_wish_count = Wish.gift_count_of_wishes(my_gift_list)
    mygift = GiftViewModel(my_gift_list, my_wish_count)
    return render_template('my_gifts.html', gifts=mygift.mygifts)

#  赠送图书视图函数


@web.route('/gifts/book/<isbn>')
@login_required
def save_to_gifts(isbn):
    if current_user.can_save_to_list(isbn):
        with db.auto_commit():
            gift = Gift()
            gift.isbn = isbn
            gift.uid = current_user.id  # current_user 实际上就是通过模型返回的USER类，里面有一个id
            gift.create_time = datetime.now()
            current_user.beans += current_app.config['BEANS_UPLOAD_ONE_BOOK']
            db.session.add(gift)  # 使用db.session来进行数据库的提交操作
    else:
        flash('您已经有书籍在赠送或者心愿清单中，请勿重复添加！')
    # 此处注意url_for的写法
    return redirect(url_for('web.book_detail', isbn=isbn))


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
