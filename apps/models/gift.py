from flask import current_app
from flask_login import current_user

from apps.apis.YuShuBook import YuShuBook
from apps.models.base import Base, db
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, desc, func
from sqlalchemy.orm import relationship, backref
import time
from datetime import datetime


class Gift(Base):
    id = Column(Integer, primary_key=True)
    user = relationship('User', backref=db.backref('gift'))  # 外键关联到user模型
    uid = Column(Integer, ForeignKey('user.id'))  # 多的这个模型，这个是外键
    isbn = Column(String(15), nullable=False)
    launched = Column(Boolean, default=False)

    @classmethod
    def recent(cls):
        '''
        :param cls
        :return 最近的30条数据，且按照时间排序去重
        '''
        recent_gifts = Gift.query.filter_by(
            launched=False).group_by(
            Gift.isbn).order_by(desc(Gift.create_time)).limit(
            current_app.config['COUNT_BOOKS']).distinct().all()
        return recent_gifts

    @classmethod
    def gift_of_mine(cls):
        '''
        通过当前用户的id返回当前用户的礼物的isbn列表
        :param:当前的用户id号
        :return: 当前的礼物的isbn列表
        '''
        uid = current_user.id
        gifts = Gift.query.filter_by(uid=uid, status=1, launched=False
                                     ).order_by(desc(Gift.create_time)
                                                ).all()
        my_gifs_isbn = [gift.isbn for gift in gifts]
        return my_gifs_isbn

    @classmethod
    def gift_count_of_my_wishes(cls, wishes_list):
        '''
        根据传入的心愿列表，统计出对应的礼物数量，并进行返回
        :param wishes_list:
        :return: dict{'isbn':xxx,'count':xxx}
        '''
        base_gift_dict = db.session.query(
            Gift.isbn,
            func.count(Gift.id)).filter(
            Gift.launched == False,
            Gift.isbn.in_(wishes_list),
            Gift.status == 1).group_by(Gift.isbn).all()

        return_dict = []
        #  将已经查询出来的结果先进行组装
        for gift in base_gift_dict:
            return_dict.append({'isbn': gift[0], 'count': gift[1]})

        #  比较不在列表中的元素，并将其添加到return_dict
        new_base_gift_list = [base[0] for base in base_gift_dict]
        diff = [x for x in wishes_list if x not in new_base_gift_list]

        for single_diff in diff:
            return_dict.append({'isbn': single_diff, 'count': 0})

        return return_dict

    @classmethod
    def book(cls,isbn):
        """返回isbn查询出来的书籍结果"""
        yushu = YuShuBook()
        result = yushu.return_isbn(isbn)
        return result
