from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user
from ..models import User
from . import auth
from .forms import LoginForm


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
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