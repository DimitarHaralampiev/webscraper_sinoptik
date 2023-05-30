from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()


class Town(Base):
    __tablename__ = 'towns'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    current_weather = relationship('CurrentWeather', back_populates='town')
    forecast_weather = relationship('ForecastWeather', back_populates='town')


class CurrentWeather(Base):
    __tablename__ = 'current_weather'
    id = Column(Integer, primary_key=True)
    town_id = Column(Integer, ForeignKey('town.id'))
    current_time = Column(DateTime, default=datetime.now())
    current_temperature = Column(Float)
    weather_condition = Column(Float)
    wind = Column(String)
    humidity = Column(Integer)

    town = relationship('Town', back_populates='current_weather')


class ForecastWeather(Base):
    __tablename__ = 'forecast_weather'
    id = Column(Integer, primary_key=True)
    town_id = Column(Integer, ForeignKey('town.id'))
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
    def __init__(self):
        self.engine = create_engine('sqlite:///weather_data.db')
        Base.metadata.bind = self.engine
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def close(self):
        """
        Close database session
        """
        self.session.close()