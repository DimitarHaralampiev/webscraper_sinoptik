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
    weather_condition = Column(Float)
    wind = Column(String)
    humidity = Column(Integer)


class ForecastWeather(Base):
    __tablename__ = 'forecast_weather'
    id = Column(Integer, primary_key=True)
    town_name = Column(String)
    current_time = Column(DateTime, default=datetime.now())
    forecast_date = Column(DateTime)
    high_temperature = Column(Float)
    low_temperature = Column(Float)
    wind = Column(String)
    humidity = Column(Integer)


class SQLHelper:
    """
    A helper class for SQLite operations.
    """
    def __init__(self, database_name: str):
        self.engine = create_engine(f'sqlite:///{database_name}')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def add_current_weather_data(self, data):
        """
        Adds current weather data to the SQLite database.

        Args:
            data (dict): A dictionary containing current weather data.
        """
        session = self.Session()
        current_weather = CurrentWeather(**data)
        session.add(current_weather)
        session.commit()

    def add_forecast_weather_data(self, data):
        """
        Adds forecast weather data to the SQLite database.

        Args:
        data (dict): A dictionary containing forecast weather data.
        """
        session = self.Session()
        forecast_weather = ForecastWeather(**data)
        session.add(forecast_weather)
        session.commit()


