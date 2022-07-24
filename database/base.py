from databases import Database
from sqlalchemy import create_engine,MetaData
from core import config

settings = config.Setting()

database = Database(settings.DB_URL)
metadata = MetaData()
engine = create_engine(settings.DB_URL)