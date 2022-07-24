from sqlalchemy import Table, Column, Integer, String, Boolean, DateTime

from datetime import datetime

from database.base import metadata

user = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String),
    Column('login', String, unique=True),
    Column('position', String),
    Column('password', String),
    Column('active', Boolean, default=True),
    Column('created_at', DateTime, default=datetime.utcnow()),
    Column('updated_at', DateTime, default=datetime.utcnow())
)