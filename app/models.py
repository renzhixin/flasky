from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from flask_login import UserMixin
from . import login_manager # login_manager是在app.init文件中定义
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app


@login_manager.user_loader
def load_user(user_id):
    """
    login manager.user loader装饰器把这个函数注册给Flask-Login，在这个扩展在需要获取已登录用户的信息时调用。
    缺少这个函数注册则Flask-login无法获取我们当前的用户
    """
    return User.query.get(int(user_id))


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        raise AttributeError('password is not a Readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        """
        生成邮箱认证的令牌
        :param expiration: 令牌过期时间，默认3600秒
        :return: dumps()方法为指定的数据生成一个加密签名，然后再对数据和签名进行序列化，生成令牌字符串。
        """
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    def confrim(self, token):
        """
        确认令牌的有效性
        :param token: 用户通过hhtps请求带来的令牌字符串
        :return: 返回令牌是否有效
        """
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confrimed = True
        db.session.add(self)
        return True

    def __repr__(self):
    	return '<Role %r>' % self.username