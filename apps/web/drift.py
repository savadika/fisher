from flask import url_for, render_template, flash, request
from flask_login import login_required, current_user
from werkzeug.utils import redirect

from apps import db
from apps.forms.drift import DriftForm
from apps.libs.email import send_email
from apps.libs.enums import PendingStatus
from apps.models.drift import Drift
from apps.models.gift import Gift
from . import web

__author__ = '七月'


@web.route('/drift/<int:gid>', methods=['GET', 'POST'])
@login_required
def send_drift(gid):
    """
    向他人请求书籍，如果满足3个条件就可以填写数据完成交易：
    1 自己不能向自己请求书籍(判断当前的礼物是不是自己的)
    2 自己鱼豆的数量必须大于1（让用户多上传）
    3 每索取两本图书，自己必须送出一本图书（让用户之间多交易）
    4 满足以上条件，则进行保存
    :param gid:传入gid
    :return:跳转到交易成功页面
    """
    mygift = Gift.query.get_or_404(gid)
    if request.method == "GET":
        if mygift.uid == current_user.id:
            flash('亲，自己不能向自己赠送书籍哦，请不要调皮！')
            return redirect(url_for('web.book_detail', isbn=mygift.isbn))
        if current_user.beans <= 1:
            flash('亲，您的鱼豆数量小于1，每上传一本书籍可以增加0.5个鱼豆哦！')
            return redirect(url_for('web.book_detail', isbn=mygift.isbn))
        if current_user.can_send_drift():
            # 不采用viewmodel，利用直接返回字典的方式来进行查询
            gifter = mygift.user.summary
            # 如果用户能发起交易，则跳转到鱼漂页面
            return render_template(
                'drift.html',
                gifter=gifter,
                user_beans=current_user.beans)
        else:
            # 否则判断为鱼豆不够，不能发起交易
            return render_template(
                'not_enough_beans.html',
                beans=current_user.beans)
    if request.method == "POST":
        drift_form = DriftForm(request.form)
        flag = drift_form.validate()
        if drift_form.validate():
            save_drift(drift_form, mygift)
            # 成功请求书籍以后，向书籍的所有者发送一封电子邮件
            # send_email(
            #     mygift.user.email,
            #     '有人想要一本书',
            #     'email/get_gift.html',
            #     wisher=current_user,
            #     gift=mygift)
    return redirect(url_for('web.index'))


@web.route('/pending')
def pending():
    pass


@web.route('/drift/<int:did>/reject')
def reject_drift(did):
    pass


@web.route('/drift/<int:did>/redraw')
def redraw_drift(did):
    pass


@web.route('/drift/<int:did>/mailed')
def mailed_drift(did):
    pass


# --------------------------------------------------------------------

def save_drift(drift_form, mygift):
    """保存交易信息方法"""
    with db.auto_commit():
        drift = Drift()
        result = Gift.book(mygift.isbn)
        # 在数据一致的前提下，将drift_form中的字段保存到drift模型中
        drift_form.populate_obj(drift)
        # 书籍信息
        drift.isbn = result['isbn']
        drift.book_title = result['title']
        drift.book_author = result['author']
        drift.book_img = result['image']
        # 赠送人信息
        drift.gifter_id = mygift.user.id
        drift.gifter_nickname = mygift.user.nickname
        drift.gift_id = mygift.id
        # 索要人信息
        drift.requester_id = current_user.id
        drift.requester_nickname = current_user.nickname
        # 状态值
        pending = PendingStatus.Waiting
        db.session.add(drift)
        # 用户的鱼豆-1
        current_user.beans -= 1
