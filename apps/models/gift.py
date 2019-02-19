
from apps.models.base import Base, db
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship, backref


class Gift(Base):
    id = Column(Integer, primary_key=True)
    user = relationship('User', backref=db.backref('gift'))  # 外键关联到user模型
    uid = Column(Integer, ForeignKey('user.id'))  # 多的这个模型，这个是外键
    isbn = Column(String(15), nullable=False)
    launched = Column(Boolean, default=False)
