import sqlalchemy
from .db_session import SqlAlchemyBase


class UserRole(SqlAlchemyBase):
    __tablename__ = 'users_roles'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    role_name = sqlalchemy.Column(sqlalchemy.String)
