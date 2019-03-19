from flask import current_app
from flask_login import current_user

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
        # 组装成需要的字典模式

        return_dict = []
        for single_wish in wishes_list:
            for gift_list in base_gift_dict:
                if single_wish == gift_list[0]:
                    return_dict.append(
                        {'isbn': gift_list[0], 'count': gift_list[1]})
                else:
                    new_dict = {'isbn': single_wish, 'count': 0}
                    return_dict.append(new_dict)

        return return_dict
