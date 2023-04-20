from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data import db_session
from data.categories import Category
from data.users import User
from data.recipes import Recipes
from forms.user import RegisterForm
from forms.user_login import LoginForm
from forms.recipe_form import RecipeForm

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
def index():
    db_sess = db_session.create_session()
    recipes = db_sess.query(Recipes).all()
    return render_template('index.html', recipes=recipes, title='Домашняя страница')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            user_role=form.role.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/recipe/<int:recipe_id>')
def show_one_recipe(recipe_id):
    db_sess = db_session.create_session()
    recipe = db_sess.query(Recipes).get(recipe_id)
    return render_template('recipe.html', title=f'{recipe.title}', recipe=recipe)


@app.route('/add_recipe',  methods=['GET', 'POST'])
@login_required
def add_recipe():
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    categories = db_sess.query(Category).all()
    res = []
    for item in categories:
        res.append((item.id, item.name))
    form = RecipeForm()
    form.categories.choices = res
    if form.validate_on_submit():
        recipe = Recipes()
        recipe.title = form.title.data
        recipe.description = form.description.data
        recipe.ingredients = form.ingredients.data
        recipe.recipe = form.recipe.data
        recipe.picture_name = form.picture.name
        category = db_sess.query(Category).get(form.categories.data)
        category.recipes.append(recipe)
        db_sess.merge(category)
        recipe.categories = [category]
        user.recipes.append(recipe)
        db_sess.merge(user)
        db_sess.commit()
        return redirect('/')
    return render_template('add_recipe.html', title='Добавление рецепта',
                           form=form)


def main():
    db_session.global_init('db/recipe_book.db')
    app.run()


if __name__ == '__main__':
    main()
