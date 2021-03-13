from datetime import datetime
from flask import Flask, render_template, request, session, redirect, url_for, flash

from . import main
from .forms import NameForm
from .. import db
from ..models import User


@main.route('/', methods=['get', 'post'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', current_time=datetime.utcnow(), form=form, name=session.get('name'))

