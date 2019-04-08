from flask import url_for, render_template, flash, request
from flask_login import login_required, current_user
from sqlalchemy import desc, or_
from werkzeug.utils import redirect

from apps import db
from apps.forms.drift import DriftForm
from apps.libs.email import send_email
from apps.libs.enums import PendingStatus
from apps.models.drift import Drift
from apps.models.gift import Gift
from apps.models.user import User
from apps.models.wish import Wish
from apps.view_models.drift import DriftViewModel
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
    title = Gift.book(mygift.isbn)['title']
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
            send_email(
                mygift.user.email,
                '有人想要一本书',
                'email/get_gift.html',
                wisher=current_user,
                gift=mygift,
                title=title)
            flash('已有一封邮件发送到赠书者的邮箱，请耐心等待哦！')
            return redirect(url_for('web.pending'))
    return redirect(url_for('web.index'))


@web.route('/pending')
@login_required
def pending():
    """返回我作为赠送者或者作为请求者的交易信息记录"""
    # fllter里面的查询条件的值需要带上所有的Drift的前缀
    drifts = Drift.query.filter(
        or_(Drift.requester_id == current_user.id,
            Drift.gifter_id == current_user.id)).order_by(
        desc(Drift.create_time)).all()
    mydrifts = DriftViewModel(drifts, current_user.id)
    return render_template('pending.html', drifts=mydrifts.data)


@web.route('/drift/<int:did>/reject')
@login_required
def reject_drift(did):
    """
    （赠送者）拒绝当前的交易
    :param did: 礼物id号
    :return:返回拒绝信息到当前的页面
    """
    with db.auto_commit():
        drift = Drift.query.filter(
            Drift.id == did, Gift.uid == current_user.id).first_or_404()
        drift.pending = PendingStatus.Reject.value
    # 如果拒绝了这个交易，那么请求者的鱼豆需要+1(将鱼豆还给他)
        requester = User.query.get_or_404(drift.requester_id)
        requester.beans += 1
    return redirect(url_for('web.pending'))


@web.route('/drift/<int:did>/redraw')
def redraw_drift(did):
    """
    撤销当前的交易
    :param did:
    :return:
    为了防止超权现象(通过自定义的URL来操作别人的鱼漂)，还必须加一个requester.id =current_user.id
    """
    with db.auto_commit():
        drift = Drift.query.filter_by(
            id=did, requester_id=current_user.id).first_or_404()
        # 需要特别注意的是，直接读取PendingStatus.Redraw读出来的是枚举类型，需要增加.value才是真实的值
        drift.pending = PendingStatus.Redraw.value
        current_user.beans += 1
    return redirect(url_for('web.pending'))


@web.route('/drift/<int:did>/mailed')
def mailed_drift(did):
    """
    点击已邮寄，完成此次交易，注意，要讲赠送清单与心愿清单同样撤销掉
    :param did:
    :return:
    """
    with db.auto_commit():
        drift = Drift.query.filter_by(id=did).first_or_404()
        drift.pending=PendingStatus.Success.value
        # 撤销赠送者的礼物(Gift)
        gift = Gift.query.filter_by(id=drift.gift_id).first_or_404()
        gift.launched=True
        # 撤销请求者的心愿（Wish）
        wish = Wish.query.filter_by(
            isbn=drift.isbn,uid=drift.requester_id,launched=False).first_or_404()
        wish.launched=True
    return redirect(url_for('web.pending'))

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
