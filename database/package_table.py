from sqlalchemy import Table, Column, Integer, String, Boolean, DateTime, ForeignKey, Float

from datetime import datetime

from database.base import metadata

package = Table(
    'packages', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', Integer, ForeignKey('users.id'), nullable=False),
    Column('weight', Float),
    Column('comment', String),
    Column('created_at', DateTime, default=datetime.utcnow()),
    Column('updated_at', DateTime, default=datetime.utcnow())
)