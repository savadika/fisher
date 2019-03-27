# -*- coding: utf-8 -*-#

# -------------------------------------------------------------------------------
# Name:         drift
# Description:  drift交易界面验证类
# Author:       ylf
# Date:         2019-03-27
# -------------------------------------------------------------------------------

from wtforms import Form, StringField
from wtforms.validators import Length, Regexp, DataRequired


class DriftForm(Form):
    """dirft交易界面验证类"""
    recipient_name = StringField(
        validators=[
            DataRequired(),
            Length(
                min=2,
                max=20,
                message="姓名2-20个字符")])
    mobile = StringField(
        validators=[
            DataRequired(),
            Regexp(
                '^1[0-9]{10}$',
                0,
                '请输入正确的手机号')])
    address = StringField(
        validators=[
            DataRequired(),
            Length(
                min=5,
                max=70,
                message="请输入至少5位地址")])
    message = StringField()
