from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from ..models import User


class LoginForm(FlaskForm):
    email = StringField('邮箱地址', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('提交')


class RegistrationForm(FlaskForm):
    email = StringField('邮箱地址', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('用户名', validators=[DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$',
                                                                                    0, '用户名必须以字母开头，且只能包含.或_')])
    password = PasswordField('密码', validators=[DataRequired(), EqualTo('confirm_password', '密码不一致')])
    confirm_password = PasswordField('再次输入密码', validators=[DataRequired()])
    submit = SubmitField('提交')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经注册过！')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('该用户名已经存在！')

