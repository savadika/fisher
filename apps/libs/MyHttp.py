# -*- coding:utf-8 -*-

# 模拟发送HTTP请求类(底层)
# from urllib import request
import requests

# ------------------几个知识点：
# 1  类的继承object在python2 和python3 里面是不同的，3里面不受影响
# 2  静态类方法，类方法，实例方法，什么时候用：看有没有用到
# 3  requests 和 urllib的区别，用requests更加方便
# 4  三元运算符怎么写？


class HttpService:
    # 通过api返回函数
    @staticmethod
    def get_result_by_url(url, return_json=True):
        result = requests.get(url)
        # 根据变量控制返回的函数是否需要转为json
        if return_json:
            return result.json()
        else:
            return result.text()
