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




