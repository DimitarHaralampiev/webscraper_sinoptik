import csv
from datetime import datetime
import pandas as pd

from sqlalchemy import Column, Integer, String, DateTime, Float, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()


class CurrentWeather(Base):
    __tablename__ = 'current_weather'
    id = Column(Integer, primary_key=True)
    town_name = Column(String)
    current_time = Column(DateTime, default=datetime.now())
    current_temperature = Column(Float)
    weather_condition = Column(String)
    wind = Column(String)
    humidity = Column(Integer)


class ForecastWeather(Base):
    __tablename__ = 'forecast_weather'
    id = Column(Integer, primary_key=True)
    town_name = Column(String)
    current_time = Column(DateTime, default=datetime.now())
    forecast_date = Column(DateTime)
    high_temperature = Column(String)
    low_temperature = Column(String)
    wind = Column(String)
    humidity = Column(String)


class SQLHelper:
    """
    A helper class for SQLite operations.
    """

    def __init__(self, database_name: str):
        self.database_name = database_name

    def create_tables(self):
        engine = create_engine(f'sqlite:///{self.database_name}')
        Base.metadata.create_all(engine)

    def create_session(self, engine):
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