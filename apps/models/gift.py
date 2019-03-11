from flask import current_app

from apps.models.base import Base, db
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, desc
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
