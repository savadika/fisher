# -*- coding:utf-8 -*-

from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery
from sqlalchemy import Column, SmallInteger, String
from contextlib import contextmanager
from datetime import datetime
# 重度改写SQLAlchemy类，来新增一个方法实现自动处理异常


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e


# 高级应用：改写fiter_by函数，实现自己的应用逻辑
# 1 要搞清楚filter_by的继承关系,
# 2 如何显示基类的改写，了解kwargs

class ylfQuery(BaseQuery):
    def filter_by(self, **kwargs):
        if 'status' not in kwargs.keys():
            kwargs['status'] = 1
        return super(ylfQuery, self).filter_by(**kwargs)


# 实例化sqlalchemy的时候自动采用我自己定义的ylfQuery来实现对
# status的加入
db = SQLAlchemy(query_class=ylfQuery)


class Base(db.Model):
    # 不想实例化就增加这条
    __abstract__ = True
    # 需要增加的公共属性
    status = Column(SmallInteger, default=1)
    # 记录的创建时间，但是有些时候不一定需要
    create_time = Column(String(200), nullable=False)

    # 定义基类的初始化
    # 如果我是在default中定义的，那么每个create_time都是一样的
    # 这个就是类变量和实例变量的区别之一
    def __init__(self):
        self.create_time = datetime.now().timestamp()

    # 定义一个共有的方法来完成属性的快速赋值

    def set_attrs(self, attrs_dict):
     """
     自动设置属性值
     :param attrs_dict:字典
     :return:NONE
     """
        for key, value in attrs_dict.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)
