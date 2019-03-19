from . import web
from flask import render_template, request, redirect, url_for, flash
from apps.forms.register import RegisterForm, LoginFrom, ResetPassword, ConfirmPassword
from apps.models.user import User
from apps.models.base import db
from flask_login import login_user, logout_user

__author__ = 'ylf'


@web.route('/register', methods=['GET', 'POST'])
def register():
    validate_form = RegisterForm(request.form)
    if request.method == 'GET':
        pass
    if request.method == 'POST' and validate_form.validate():
        with db.auto_commit():
            user = User()
            user.set_attrs(validate_form.data)
            db.session.add(user)
        return redirect(url_for('web.login'))  # 这个地方也必须要做一个return 返回才可以
    return render_template('auth/register.html', form=validate_form)


@web.route('/login', methods=['GET', 'POST'])
def login():
    validate_form = LoginFrom(request.form)
    if request.method == 'POST' and validate_form.validate():
        # 表单规则验证通过，查询是否存在user数据记录
        user = User.query.filter_by(email=validate_form.email.data).first()
        # 如果存在且密码一致
        if user and user.check_password(validate_form.password.data):
            # 开始进行cookie的处理,写入到cookie
            login_user(user, remember=True)
            # 跳转回原页面的处理
            # 获取url中的参数就是登陆参数
            # 如果next不存在且不是一个url地址，则跳向首页，否则跳向next
            next = request.args.get('next')
            if not next or not next.startwith('/'):
                next = url_for('web.index')
            return redirect(next)
        else:
            flash('用户名或者密码不存在！')
    return render_template('auth/login.html', form={'data': {}})


@web.route('/reset/password', methods=['GET', 'POST'])
def forget_password_request():
    '''
    密码找回功能
    :return:
    '''
    validate_form = ResetPassword(request.form)
    if request.method == 'POST':
        if validate_form.validate():
            # first_or_404如果返回的对象不存在，可以直接抛出404异常
            # 有助于判空操作，结合aop面向切面编程，可以减少代码量
            user = User.query.filter_by(
                email=validate_form.email.data).first_or_404()
            from apps.libs.email import send_email
            send_email(validate_form.email.data,
                       '请重置你的密码',
                       'email/reset_password.html',
                       user=user,
                       token=user.generate_token())
    return render_template('auth/forget_password_request.html',form=validate_form)


@web.route('/reset/password/<token>', methods=['GET', 'POST'])
def forget_password(token):
    validate_password = ConfirmPassword(request.form)
    if request.method == 'POST' and validate_password.validate():
        if User.reset_password(token,validate_password.password1.data):
            flash('密码已经重置')
            return  redirect(url_for('web.login'))
        else:
            flash('密码重置失败！')
            return redirect(url_for('web.login'))
    return render_template('auth/forget_password.html')


@web.route('/change/password', methods=['GET', 'POST'])
def change_password():
    pass


@web.route('/logout')
def logout():
    '''
    用户登出功能
    :return:
    '''
    logout_user()
    return redirect(url_for('web.index'))
