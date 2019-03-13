
from apps.models.base import Base, db
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, func
from sqlalchemy.orm import relationship, backref


class Wish(Base):
    id = Column(Integer, primary_key=True)
    user = relationship('User', backref=db.backref('wish'))  # 外键关联到user模型
    uid = Column(Integer, ForeignKey('user.id'))  # 多的这个模型，这个是外键
    isbn = Column(String(15), nullable=False)
    launched = Column(Boolean, default=False)

    @classmethod
    def gift_count_of_wishes(cls, isbn_list):
        '''
        根据isbn列表查询出对应的wish,并统计出对应的数量，组成列表，然后转换成字典供外部调用
        跨表的查询，最好用的是db.session.filter()
        :param isbn_list:
        :return: [{'isbn':,'count':}]
        '''
        base_wish_dict=db.session.query(
            Wish.isbn,
            func.count(Wish.id)).filter(
            Wish.launched == False,
            Wish.isbn.in_(isbn_list),
            Wish.status == 1).group_by(
            Wish.isbn).all()

        return_wish_dict = [ {'isbn':wish_dict[0],'count':wish_dict[1]} for wish_dict in base_wish_dict]
        return  return_wish_dict
