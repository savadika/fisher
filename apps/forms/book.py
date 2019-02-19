# -*- coding:utf-8 -*-

from wtforms import Form, StringField, IntegerField
from wtforms.validators import Length, NumberRange


class SearchForms(Form):
    q = StringField(validators=[Length(min=1, max=30)])
    # 如果客户端不传page参数，则默认设置为1
    page = IntegerField(validators=[NumberRange(min=1, max=99)], default=1)
