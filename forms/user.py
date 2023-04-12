from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, SelectField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    surname = StringField('Фамилия', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    role = SelectField('Ваша роль', coerce=int,
                       choices=[(1, 'обычный пользователь'), (2, 'создатель рецептов')])
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')
