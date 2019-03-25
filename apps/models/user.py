from flask import current_app

from apps.models.base import Base, db
from sqlalchemy import Column, String, Boolean, Float, Integer
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from apps import login_manager
from ..libs.helper import is_isbn_or_key
from ..apis.YuShuBook import YuShuBook
from .gift import Gift
from .wish import Wish
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


class User(Base, UserMixin):
    id = Column(Integer, primary_key=True)
    nickname = Column(String(24), nullable=False)
    phone_number = Column(String(18), unique=True)
    _password = Column('password', String(128))  #定义列名
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
        # 这个id的用户有赠送或者索要该书籍，则不能再赠送
        gifting = Gift.query.filter_by(
            uid=self.id, isbn=isbn,launched=False).first()
        wishing = Wish.query.filter_by(
            uid=self.id, isbn=isbn, launched=False).first()
        if gifting or wishing:
            return False
        else:
            return True



    def generate_token(self,expration=600):
        '''
        定义重置密码时token的生成，可以用来进行加密id的操作
        :param expration:过期时间，默认600秒
        :return:
        '''
        s = Serializer(current_app.config['SECRET_KEY'],expration)
        return s.dumps({'id':self.id}).decode('utf-8')

    @classmethod
    def reset_password(cls,token,new_password):
        '''
        根据token以及新密码，来重置用户的密码
        :param token: 用户的token
        :param new_password: 新密码
        :return: 返回是否成功的状态值
        '''
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data=s.loads(token.encode('utf-8'))
        except:
            return False
        uid = data.get('id')
        with db.auto_commit():
            user = User.query.get(uid)
            user.password = new_password
        return  True


# 此处不理解，虽然是强制要求实现的，但是为什么需要加这个，加了这个有什么意义？
@login_manager.user_loader
def load_user(uid):
    return User.query.get(int(uid))
