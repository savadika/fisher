# 普通方法实现上下文管理器，比较容易理解，但是复用性差
from contextlib import contextmanager


class gogo(object):
    def __enter__(self):
        print('this is enter ----')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('this is exiting -----')

    def query(self):
        print('this is using query')


with gogo() as glo:
    glo.query()


# ------------使用contextmanager来实现上下文管理器，不太好理解，但是复用性高---------

# 基类

class newgogo(object):
    def query(self):
        print('this is new query')

# 上下文管理器


@contextmanager
def my_newgogo():
    print('this is enter-----')
    yield newgogo()
    print('this is exciting -----')


# 调用基类的方法
with my_newgogo() as r:
    r.query()
