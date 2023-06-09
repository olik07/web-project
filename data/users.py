import datetime
import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash

from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_role = sqlalchemy.Column(sqlalchemy.Integer,
                                  sqlalchemy.ForeignKey('users_roles.id'))
    role = orm.relationship('UserRole')
    recipes = orm.relationship('Recipes', back_populates='user')
    favorite_recipes = orm.relationship('Recipes',
                                        secondary="favorite_recipes",
                                        backref="users", lazy="subquery")
    surname = sqlalchemy.Column(sqlalchemy.String)
    name = sqlalchemy.Column(sqlalchemy.String)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String)
    modified_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                      default=datetime.datetime.now)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def favorite_ids(self):
        favorite_ids = list(map(lambda i: i.id, self.favorite_recipes))
        return favorite_ids


favorite_recipes = sqlalchemy.Table(
    'favorite_recipes',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('recipe', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('recipes.id')),
    sqlalchemy.Column('user', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('users.id'))
)
