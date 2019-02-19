# -*- coding:utf-8 -*-


def is_isbn_or_key(q):
    """判断q是ISBN还是关键字"""
    # 1  13位纯数字
    isbn_or_key = 'key'
    if len(q) == 13 and q.isdigit():
        isbn_or_key = 'isbn'
    # 2  10位数字中间夹杂 -
    else:
        short_q = q.replace('-', '')
        if len(short_q) == 10 and short_q.isdigit():
            isbn_or_key = 'isbn'
        else:
            isbn_or_key = 'key'
    return isbn_or_key


def getBookByIsbn(isbn):
    """通过isbn来获取数据"""
    url = 'http://t.yushu.im/v2/book/isbn/{isbn}'
    # url 变量转化
    select_url = url.format(isbn)
    return select_url
    pass


