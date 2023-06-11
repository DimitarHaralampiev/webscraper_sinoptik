import csv
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.current_weather import Base, current_weather
from models.forecast_weather import Base, forecast_weather


class SQLHelper:
    """
    A helper class for SQLite operations.
    """

    def __init__(self, database_name: str):
        self.database_name = database_name

    def __create_session(self, engine):
        """
        Create a session using the provided SQLAlchemy engine.

        Args:
            engine: The SQLAlchemy engine to bind the session to.

        Returns:
            The created session object.
        """
        Session = sessionmaker(bind=engine)
        session = Session()
        return session

    def create_tables(self):
        engine = create_engine(f'sqlite:///{self.database_name}')
        Base.metadata.create_all(engine)

