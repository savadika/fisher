# 实现上下文管理器
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
