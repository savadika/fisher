# -*- coding:utf-8 -*-

# 使用viewmodel来对数据进行统一返回处理,返回给前端进行展示
# returned
# ={"books"[]:[title,publisher,pages,price,summary,image],"total":,"keyword"}


class BookViewModel:

    # 最终要返回的数据结构
    returned = {
        'books': [],
        'total': 0,
        'keyword': ''
    }

    # 组装isbn查询出来的单本的数据

    def get_isbn_book(self, data, keyword=''):
        if data:
            self.returned['total'] = 1
            self.returned['keyword'] = keyword
            self.returned['books'] = [self.get_single_book(data)]
        return self.returned

    # 组装key查询出来的多本的数据

    def get_key_books(self, data, keyword):
        self.returned['total'] = data['total']
        self.returned['keyword'] = keyword
        more_book = []
        for book in data['books']:
            more_book.append(self.get_single_book(book))
        self.returned['books'] = more_book
        return self.returned

    # 传入单本的data，就可以对数据进行裁剪，封装

    def get_single_book(self, data):
        return_book = {}
        return_book['title'] = data['title']
        return_book['publisher'] = data['publisher']
        return_book['pages'] = data['pages']
        return_book['price'] = data['price']
        return_book['summary'] = data['summary']
        return_book['image'] = data['image']
        return_book['isbn'] = data['isbn']
        return_book['author'] = '，'.join(data['author'])

        # 对书籍进行综合的封装，采用lambda,列表表达式，函数式编程，property等综合概念
        # 思路： 用lambda匿名函数来判断x是否为空，用filter来将结果为True的列表中的值取出来
        # 思路： 将列表中的数进行拼接,注意，python3返回的是fliter对象，需要用list()进行转化
        fliterdata = filter(
            lambda x: True if x else False, [
                return_book['author'], data['publisher'], data['price']])
        newdata = list(fliterdata)
        return_book['showstring'] = '/'.join(newdata)

        return return_book
