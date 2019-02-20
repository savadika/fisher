# -*- coding:utf-8 -*-

from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy
from sqlalchemy import Column, SmallInteger
from contextlib import contextmanager
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


db = SQLAlchemy()


class Base(db.Model):
    # 不想实例化就增加这条
    __abstract__ = True
    # 需要增加的公共属性
    status = Column(SmallInteger, default=1)

    # 定义一个共有的方法来完成属性的快速赋值
    def set_attrs(self, attrs_dict):
        for key, value in attrs_dict.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)
