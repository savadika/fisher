# -*- coding:utf-8 -*-

'''
定义一个电子邮件的发送方法
'''
from threading import Thread

from flask import current_app, render_template
from flask_mail import Message
from apps import mail


def sync_send_mail(newapp, msg):
    with newapp.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            pass


def send_email(to, subject, template, **kwargs):
    '''
    定义电子邮件的发送方法
    :param to: 发送给谁
    :param subject: 主题
    :param template: 内容模板
    :param **kwargs 定义一些其他的变量内容
    :return:
    '''
    # 定义message的基本格式
    msg = Message('[鱼书]' + '' + subject,
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[to])
    # 定义邮件的模板发送格式
    msg.html = render_template(template, **kwargs)
    # 开启一个线程，来异步发送电子邮件
    flaskapp = current_app._get_current_object()
    thr = Thread(target=sync_send_mail, args=[flaskapp, msg])
    thr.start()
