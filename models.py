from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, create_engine
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

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

    town = relationship('Town', back_populates='current_weather')


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

    town = relationship('Town', back_populates='forecast_weather')


class SQLHelper:
    """
    A helper class for SQLite operations.
    """
    def __init__(self, database_name):
        self.engine = create_engine(f'sqlite:///{database_name}')
        Base.metadata.bind = self.engine
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def close(self):
        """
        Close database session
        """
        self.session.close()