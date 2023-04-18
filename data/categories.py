import sqlalchemy
from .db_session import SqlAlchemyBase


association_table = sqlalchemy.Table(
    'recipe_to_category',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('recipe', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('recipes.id')),
    sqlalchemy.Column('category', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('categories.id'))
)


class Category(SqlAlchemyBase):
    __tablename__ = 'categories'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
