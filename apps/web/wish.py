from datetime import datetime

from flask import url_for, flash, render_template
from flask_login import current_user
from werkzeug.utils import redirect

from apps import db
from apps.models.gift import Gift
from apps.models.wish import Wish
from apps.view_models.wish import WishViewModel
from . import web

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
    pass


@web.route('/wish/book/<isbn>/redraw')
def redraw_from_wish(isbn):
    pass
