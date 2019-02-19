# -*- coding:utf-8 -*-

from wtforms import StringField, PasswordField, Form
from wtforms.validators import Length, DataRequired, Email, ValidationError
from apps.models.user import User


class RegisterForm(Form):
    # 此处定义数据字段的基本验证工作
    email = StringField(
        validators=[
            DataRequired(), Length(
                8, 64), Email(
                message='电子邮件不符合规则')])
    nickname = StringField(
        validators=[
            Length(
                5,
                30,
                message='字符数在5-20之间'),
            DataRequired()])
    password = PasswordField(
        validators=[
            DataRequired(), Length(
                6, 20, message='密码在6-20位之间')])

    # 此处自定义验证器规则来满足具体的业务需要
    # 1  验证email是否已经存在于数据库中，进行数据库的查询
    # 方法：既可以采用db.session来进行查询，也可以使用更加方便的方式来进行
    # 具体：方法必须以validate_开头

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('email已经存在')

    # 自定义属性：nickname不能重复
    def validate_nickname(self, field):
        if User.query.filter_by(nickname=field.data).first():
            raise ValidationError('nickname已经存在')


class LoginFrom(Form):
    email = StringField(
        validators=[
            DataRequired(), Length(
                8, 64), Email(
                message='电子邮件不符合规则')])

    password = PasswordField(
        validators=[
            DataRequired(), Length(
                6, 20, message='密码在6-20位之间')])















