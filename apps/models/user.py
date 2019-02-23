
from apps.models.base import Base
from sqlalchemy import Column, String, Boolean, Float, Integer
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from apps import login_manager
from ..libs.helper import is_isbn_or_key
from ..apis.YuShuBook import YuShuBook
from .gift import Gift
from .wish import Wish


class User(Base, UserMixin):
    id = Column(Integer, primary_key=True)
    nickname = Column(String(24), nullable=False)
    phone_number = Column(String(18), unique=True)
    _password = Column('password', String(128))
    email = Column(String(18), unique=True, nullable=False)
    confirmed = Column(Boolean, default=False)
    beans = Column(Float, default=0)
    send_counter = Column(Integer, default=0)
    receive_counter = Column(Integer, default=0)
    wx_open_id = Column(String(50), default='')
    wx_name = Column(String(50), default='')

    # 当需要进行数据预处理的时候，就可以使用 getter 和 setter

    # 此处对属性进行读取
    @property
    def password(self):
        return self._password

    # 对属性进行写入
    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    # 验证是否和_password一致

    def check_password(self, raw):
        return check_password_hash(self._password, raw)
        pass

    # 定义能否赠送礼物
    # 需要满足3个条件：
    # 1  符合isbn规范且存在在yushubook中
    # 2  不予许赠送相同的多本图书
    # 3  不能即是赠送者又是索要者
    def can_save_to_list(self, isbn):
        if not is_isbn_or_key(isbn):
            return False
        ysbook = YuShuBook()
        result = ysbook.return_isbn(isbn)
        if isinstance(result, str):
            return False
        gifting = Gift.query.filter_by(
            id=self.id, isbn=isbn, launched=False).first()
        wishing = Wish.query.filter_by(
            id=self.id, isbn=isbn, launched=False).first()
        if not gifting and not wishing:
            return True
        else:
            return False


# 此处不理解，虽然是强制要求实现的，但是为什么需要加这个，加了这个有什么意义？
@login_manager.user_loader
def load_user(uid):
    return User.query.get(int(uid))
