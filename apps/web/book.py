# -*- coding:utf-8 -*-
# book视图函数相关的类

# 定义搜索方法，看能否成功
from flask import jsonify, request, render_template, flash
from apps.apis.YuShuBook import YuShuBook
from apps.web import web
from apps.libs.helper import is_isbn_or_key
from apps.forms.book import SearchForms
from apps.view_models.book import BookViewModel
# 使用预先定义好的web蓝图来完成工作


@web.route('/book/search/')
def search():
    """接下去对q需要进行验证处理"""
    testform = SearchForms(request.args)
    newresult = ''
    if testform.validate():
        q = testform.q.data.strip()
        page = testform.page.data
        the_keyword = is_isbn_or_key(q)
        # 返回isbn的查询结果
        if the_keyword == 'isbn':
            yushu = YuShuBook()
            result = yushu.return_isbn(q)
            bookmodel = BookViewModel()
            newresult = bookmodel.get_isbn_book(result, q)
        # 返回key的查询结果
        if the_keyword == 'key':
            yushu = YuShuBook()
            result = yushu.return_key(q, page)
            bookmodel = BookViewModel()
            newresult = bookmodel.get_key_books(result, q)
    else:
        flash('您所输入的关键字存在错误！')
    return render_template('search_result.html', books=newresult)


@web.route('/book/<isbn>/detail')
def book_detail(isbn):
    yushu = YuShuBook()
    result = yushu.return_isbn(isbn)
    return render_template(
        'book_detail.html',
        book=result,
        wishes=[],
        gifts=[])
    pass


# 测试jinja2模板---------------------------------------------------------

@web.route('/test')
def test():
    r = {
        'name': 'ylf',
        'age': 22
    }
    return render_template('test.html', data=r)


@web.route('/test1')
def test1():
    d = {
        'name': '',
        'age': 18
    }
    flash('useflash successfuly!')
    return render_template('test1.html', data=d)
