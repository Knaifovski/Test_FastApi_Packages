from .user_table import user
from .package_table import package
from .base import metadata, engine

metadata.create_all(engine)