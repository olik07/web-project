from flask import Flask, render_template
from data import db_session
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
def index():
    return render_template('base.html', title='Домашняя страница')


def main():
    db_session.global_init('db/recipe_book.db')
    app.run()


if __name__ == '__main__':
    main()
