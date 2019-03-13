# -*- coding:utf-8 -*-
from apps.apis.YuShuBook import YuShuBook
from apps.models.gift import Gift


class GiftViewModel:
    '''
    定义一个我的礼物的view_model，来进行页面的适配
    :return [{id:'',book:'',count:''}]
    '''

    def __init__(self, my_gift_list, my_wishes_count):
        '''
        初始化类
        :param my_gift_list:我的礼物isbn的列表
        :param my_wish_count: 我的礼物对应的心愿数量
        '''
        self.mygifts = []
        self.__my_gift_list = my_gift_list
        self.__my_wishes_count = my_wishes_count
        self.__parse()

    def __parse(self):
        '''
        :return: 一个字典组成的列表
        '''
        for gift_isbn in self.__my_gift_list:
            # 此处又要做一个viewmodel的适配，还是写在book里面比较好
            yushu = YuShuBook()
            # 根据礼物去查询书籍信息，返回到首页
            result = yushu.return_isbn(gift_isbn)
            newsresult={}
            newsresult['author'] = result['author'][0]
            newsresult['isbn'] = result['isbn']
            newsresult['image'] = result['image']
            newsresult['title'] = result['title']
            newsresult['summary'] = result['summary']
            newsresult['publisher'] = result['publisher']
            newsresult['price'] = result['price']
            this_gift = Gift.query.filter_by(isbn=gift_isbn).first()

            if len(self.__my_wishes_count)!= 0:
                for wish in self.__my_wishes_count:
                    if gift_isbn == wish['isbn']:
                        r = {
                            'id': this_gift.id,
                            'book': newsresult,
                            'wishes_count': wish['count']
                        }
                        self.mygifts.append(r)
            else:
                r = {
                    'id': this_gift.id,
                    'book': newsresult,
                    'wishes_count': 0
                }
                self.mygifts.append(r)
        return self.mygifts
