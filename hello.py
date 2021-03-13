from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy


class NameForm(FlaskForm):
    name = StringField('Whats your name?', validators=[DataRequired()])
    submit = SubmitField('submit')


db = SQLAlchemy()


def create_flask_app(config):
    """
    创建flask应用
    :param config:配置对象
    :return: app应用
    """
    flask_app = Flask(__name__)
    flask_app.config.from_object(config)

    # 从环境变量中加载配置信息替换默认的配置
    # flask_app.config.from_envvar('PROJECT_SETTING', silent=False)

    flask_app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://renzhixin:renzhixin@localhost/postgres"
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(flask_app)

    return flask_app


class DefaultConfig(object):
    """默认应用配置信息"""
    SECRET_KEY = 'RENZHIXIN'


app = create_flask_app(DefaultConfig)


@app.route('/', methods=['get', 'post'])
def index():
    print(app.config['SECRET_KEY'])
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', current_time=datetime.utcnow(), form=form, name=session.get('name'))


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


@app.route('/comments')
def comment():
    comments = ['a', 'b', 'c']
    return render_template('comment.html', comments=comments)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


class Role(db.Model):
    tablename = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    tablename = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<Role %r>' % self.username


if __name__ == '__main__':
    bootstrap = Bootstrap(app)
    moment = Moment(app)
    app.run(host="0.0.0.0", port='5000', debug=True)
