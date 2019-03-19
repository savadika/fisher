from flask_login import current_user

from apps.models.base import Base, db
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, func, desc
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
        base_wish_dict = db.session.query(
            Wish.isbn,
            func.count(Wish.id)).filter(
            Wish.launched == False,
            Wish.isbn.in_(isbn_list),
            Wish.status == 1).group_by(
            Wish.isbn).all()

        return_dict = []
        for single_list in isbn_list:
            for wish_list in base_wish_dict:
                if single_list == wish_list[0]:
                    return_dict.append({'isbn': wish_list[0], 'count': wish_list[1]})
                else:
                    new_dict = {'isbn': single_list, 'count': 0}
                    return_dict.append(new_dict)

        return return_dict

    @classmethod
    def get_wishes_of_mine(self):
        '''
        根据当前用户的id返回心愿清单列表
        :return: 心愿清单的isbn列表
        '''
        whishes_isbn_list = []
        uid = current_user.id
        wishes_list = Wish.query.filter_by(
            uid=uid, launched=False).order_by(
            desc(
                Wish.create_time)).all()
        for wish in wishes_list:
            whishes_isbn_list.append(wish.isbn)
        return whishes_isbn_list
