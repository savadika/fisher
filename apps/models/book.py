# -*- coding:utf-8 -*-
# 一般sqlalchemy ,flask封装以后的Flask_SQLAlChemy
# install flask-sqlalchemy

from sqlalchemy import Column, Integer, String
from apps.models.base import Base
# 实例化类

class Book(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)  # 整形，主键，自增长
    title = Column(String(100), nullable=True)  # 字符型，非空
    author = Column(String(50), default='未名')  # 字符型，默认值
    publisher = Column(String(50))
    price = Column(String(20))
    page = Column(Integer)
    pubdate = Column(String(20))
    isbn = Column(String(20), nullable=True, unique=True)  # 指定唯一
    summary = Column(String(1000))
    image = Column(String(50))
