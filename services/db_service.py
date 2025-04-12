from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm.decl_api import DeclarativeMeta

from config.settings import settings

# Create the base model class
Base: DeclarativeMeta = declarative_base()

class DatabaseManager:
    def __init__(self):
        self.engine = create_async_engine(
            settings.DATABASE_URL,
            echo=True
        )

        self.async_session_maker = async_sessionmaker(
            self.engine,
            expire_on_commit=False
        )


db_manager = DatabaseManager()
__all__ = ['Base', 'db_manager']