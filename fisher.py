# -*- coding:utf-8 -*-

# 从apps的包初始化文件中导入app创建函数
from apps import create_app

if __name__ == '__main__':
    app = create_app()
    app.run()
