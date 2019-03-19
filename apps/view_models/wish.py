# -*- coding:utf-8 -*-
from apps.apis.YuShuBook import YuShuBook
from apps.models.wish import Wish


class WishViewModel:
    '''
    wish的viewmodel类，通过传入的参数，适配到wish页面
    '''

    def __init__(self, wish_list, gifts_count_of_wishes):
        '''
        通过类的方式自动生成需要的数据
        :param wish_list:wish的isbn列表
        :param gifts_count_of_wishes:wish对应的礼物的数量
        '''
        self.my_wishes = []
        self.__wish_list = wish_list
        self.__gifts_count_of_wishes = gifts_count_of_wishes
        self.__parse()
        pass

    def __parse(self):
        '''
        定义数据的转化
        :return: [{'id':xxx,'books':xxx,'count':xxx}]
        '''
        for wish_isbn in self.__wish_list:
            yushu = YuShuBook()
            # 根据礼物去查询书籍信息，返回到首页
            result = yushu.return_isbn(wish_isbn)
            newsresult = {}
            newsresult['author'] = result['author'][0]
            newsresult['isbn'] = result['isbn']
            newsresult['image'] = result['image']
            newsresult['title'] = result['title']
            newsresult['summary'] = result['summary']
            newsresult['publisher'] = result['publisher']
            newsresult['price'] = result['price']
            this_wish = Wish.query.filter_by(isbn=wish_isbn).first()
            if len(self.__gifts_count_of_wishes) != 0:
                for gift in self.__gifts_count_of_wishes:
                    if wish_isbn ==gift['isbn']:
                        r = {
                            'id': this_wish.id,
                            'book': newsresult,
                            'wishes_count': gift['count']
                        }
                        self.my_wishes.append(r)
            else:
                r = {
                    'id': this_wish.id,
                    'book': newsresult,
                    'wishes_count': 0
                }
                self.my_wishes.append(r)
        return self.my_wishes
