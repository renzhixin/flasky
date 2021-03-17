from datetime import datetime
from flask import Flask, render_template, request, session, redirect, url_for, flash, current_app
from . import main
from .forms import NameForm
from .. import db
from ..models import User


@main.route('/', methods=['get', 'post'])
def index():
    print(current_app.config['MAIL_SERVER'])
    print(current_app.config['MAIL_PORT'])
    print(current_app.config['MAIL_USERNAME'])
    print(current_app.config['MAIL_PASSWORD'])
    print(current_app.config['SECRET_KEY'])


    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
        else:
            session['known'] = True


        # 闪现消息
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')

        session['name'] = form.name.data
        form.name.data = ''

        return redirect(url_for('.index'))
    return render_template('index.html',
                           known=session.get('known', False),
                           current_time=datetime.utcnow(),
                           form=form,
                           name=session.get('name'))

