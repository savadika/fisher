from datetime import datetime

from flask import url_for, flash, render_template
from flask_login import current_user
from werkzeug.utils import redirect

from apps import db
from apps.libs.email import send_email
from apps.models.gift import Gift
from apps.models.user import User
from apps.models.wish import Wish
from apps.view_models.wish import WishViewModel
from . import web
from apps.apis.YuShuBook import YuShuBook

__author__ = '七月'


@web.route('/my/wish')
def my_wish():
    '''
    我的心愿清单
    :return:
    '''
    wish_isbn_list = Wish.get_wishes_of_mine()
    gifts_of_wishes = Gift.gift_count_of_my_wishes(wish_isbn_list)
    gifts = WishViewModel(wish_isbn_list, gifts_of_wishes)
    return render_template('my_wish.html', wishes=gifts.my_wishes)

# 保存到心愿清单


@web.route('/wish/book/<isbn>')
def save_to_wish(isbn):
    if current_user.can_save_to_list(isbn):
        with db.auto_commit():
            wish = Wish()
            wish.isbn = isbn
            wish.uid = current_user.id
            wish.create_time = datetime.now()
            db.session.add(wish)
    else:
        flash('您已经有书籍在赠送或者心愿清单中，请勿重复添加！')
    return redirect(url_for('web.book_detail', isbn=isbn))


@web.route('/satisfy/wish/<int:wid>')
def satisfy_wish(wid):
    """
    向他人赠送书籍
    :param wid:wish的id号
    :return: 返回wish页面
    """
    # 两种查询方法之一：使用fliter_by需要查询两次，但是次数需要用到很多的数据，所以用第一种
    wish = Wish.query.filter_by(id=wid).first()
    wisher = User.query.filter_by(id=wish.uid).first()
    gift = Gift.query.filter_by(isbn=wish.isbn, uid=current_user.id).first()
    gifter = User.query.filter_by(id=gift.uid).first()
    yushu = YuShuBook()
    book = yushu.return_isbn(wish.isbn)
    # 使用fliter只要一次查询即可，fliter使用于跨表的查询
    # testuser=User.query.filter(Wish.id==wid).first()
    send_email(
        wisher.email,
        '有人想把书籍赠送给您',
        'email/satisify_wish.html',
        wisher=wisher,
        gift=gift,
        gifter=gifter,
        book=book
    )
    flash('已经有一封邮件发送到对方的邮箱')
    return redirect(url_for('web.book_detail', isbn=wish.isbn))


@web.route('/wish/book/<isbn>/redraw')
def redraw_from_wish(isbn):
    """
    撤销心愿
    :param isbn:当前的书籍编号
    :return: 跳转到当前礼物页面
    """
    wish = Wish.query.filter(
        Wish.isbn == isbn,
        Wish.launched == False,
        User.id == current_user.id).first_or_404()
    with db.auto_commit():
        wish.delete()
    return redirect(url_for('web.my_wish'))
