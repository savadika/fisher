# -*- coding:utf-8 -*-

from flask import Flask

# 导入数据库的实例
from apps.models.base import db
from flask_login import LoginManager

# 导入数据库迁移类
from flask_migrate import Migrate

# apps下app的实例化初始工作都在此完成
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object('apps.secure')
    app.config.from_object('apps.setting')
    migrate = Migrate(app, db)
    # 此处需要理解上下文的概念,使用上下文管理器来进行创建
    db.init_app(app)
    with app.app_context():
        # 创建数据库表之前需要先引入模型
        from apps.models import user, book, gift, wish
        db.create_all()

    login_manager.init_app(app)
    reg_blueprint(app)  # app上装载蓝图
    return app

#  定义app的注册蓝图的方法，这个可以等蓝图以后慢慢加


def reg_blueprint(app):
    from apps.web import web
    app.register_blueprint(web)
