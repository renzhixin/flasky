import sys
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from config import config
from flask_login import LoginManager, current_user


bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()

"""
LoginManager对象的login view属性用于设置登录页面的端点。匿名用户尝试访问受保护的页面时，Flask-Login将重定向到登录页面。
因为登录路由在蓝本中定义，所以要在前面加上蓝本的名称。
"""
login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)

	bootstrap.init_app(app)
	mail.init_app(app)
	moment.init_app(app)
	db.init_app(app)
	login_manager.init_app(app)	# 不执行此操作，则‘templates/base.html’中登录按钮的‘current_user’变量无法正确引用

	# 附加路由和自定义的错误页面

	# 注册蓝本
	from .main import main as main_blueprint
	app.register_blueprint(main_blueprint)
	# 注册身份验证蓝本
	from .auth import auth as auth_blueprint
	app.register_blueprint(auth_blueprint, url_prefix='/auth')

	# 返回app
	return app

