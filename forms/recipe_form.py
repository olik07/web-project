from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import StringField, TextAreaField, SelectField
from wtforms import FileField, SubmitField
from wtforms.validators import DataRequired

from data import db_session
from data.categories import Category


def get_all_categories():
    db_session.global_init('db/recipe_book.db')
    db_sess = db_session.create_session()
    categories = db_sess.query(Category).all()
    res = []
    for item in categories:
        res.append((item.id, item.name))
    return res


class RecipeForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    description = TextAreaField('Краткое описание', validators=[DataRequired()])
    picture = FileField('Картинка в формате jpg', validators=[FileRequired()])
    ingredients = TextAreaField('Ингредиенты (каждый с новой строки)',
                                validators=[DataRequired()])
    recipe = TextAreaField('Рецепт (каждый шаг с новой строки)',
                           validators=[DataRequired()])
    categories = SelectField('Выберите одну категорию', coerce=int,
                             choices=get_all_categories())
    submit = SubmitField('Создать рецепт')
