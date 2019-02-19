# -*- coding:utf-8 -*-
from apps.libs.MyHttp import HttpService


class YuShuBook(object):
    """用来处理业务逻辑的鱼书类，请求并返回书籍结果"""
    isbn_url = 'http://t.yushu.im/v2/book/isbn/{}'
    key_url = 'http://t.yushu.im/v2/book/search?q={}&count={}&start={}'

    # 返回isbn查询出来的结果
    def return_isbn(self, isbn):
        url = self.isbn_url.format(isbn)
        result = HttpService.get_result_by_url(url)
        if result:
            return result
        else:
            return '{"code":400,"message":"isbn not found this book"}'

    # 返回key查询出来的结果
    def return_key(self, key, page=1):
        url = self.key_url.format(key, 10, (page - 1) * 10)
        result = HttpService.get_result_by_url(url)
        if result['total'] != 0:
            return result
        else:
            return '{"code":401,"message":"key word not found this book"}'
