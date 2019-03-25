# -*- coding:utf-8 -*-
from apps.models.base import Base
from sqlalchemy import Column, Integer, String


class Drift(Base):
    """
    记录交易信息的模型
    特别需要指出的是：
    这个模型需要记录的数据必须忠实反映交易信息，因此必须合理使用数据库的数据冗余
    """

    # 交易id号

    id = Column(Integer, primary_key=True)

    # 邮寄信息
    recipient_name = Column(String(50), nullable=False)
    address = Column(String(30), nullable=False)
    message = Column(String(50))
    phone_number = Column(String(20), nullable=False)

    # 书籍信息
    isbn = Column(String(13))
    book_title = Column(String(50))
    book_author = Column(String(10))
    book_img = Column(String(50))

    # 赠送人信息
    gifter_id = Column(Integer)
    gifter_nickname = Column(String(20))
    gift_id = Column(Integer)

    # 索要人信息
    requester_id = Column(Integer)
    requester_nickname = (String(20))

    # 交易状态，利用枚举类型来进行设置
    pending = Column('pending', Integer, default=1)
