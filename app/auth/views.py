from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from ..models import User
from . import auth
from .. import db
from ..email import send_email
from .forms import LoginForm, RegistrationForm


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        print(user.username)
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)

            '''
            用户访问未授权的URL时会显示登录表单，
            Flask-Login会把原URL保存在查询字符串的next参数中，这个参数可从request.args字典中读取。
            '''
            next = request.args.get('next')
            if next is None or not next.startwith('/'):
                next = url_for('main.index')
            return redirect(next)
        # 如果用户没有提交表单
        flash('无效的用户名或密码')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required # loginr_equired装饰器可以保护路由，禁止未授权的用户访问只让通过身份验证的用户访问
def logout():
    logout_user()
    flash('你已登出')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, '账户确认', 'auth/email/confirm', user=user, token=token)
        flash('请到您注册时使用的邮箱中进行确认！')
        # flash('你已经注册成功！')
        # return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('您的账户已经确认！')
    else:
        flash('你的确认链接无效！')
    return redirect(url_for('main.index'))


