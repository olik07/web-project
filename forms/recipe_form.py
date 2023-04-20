from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from wtforms import FileField, SubmitField
from wtforms.validators import DataRequired


class RecipeForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    description = TextAreaField('Краткое описание', validators=[DataRequired()])
    picture = FileField('Картинка в формате jpg', validators=[DataRequired()])
    ingredients = TextAreaField('Ингредиенты (каждый с новой строки)',
                                validators=[DataRequired()])
    recipe = TextAreaField('Рецепт (каждый шаг с новой строки)',
                           validators=[DataRequired()])
    categories = SelectField('Выберите одну категорию', coerce=int)
    submit = SubmitField('Создать рецепт')
