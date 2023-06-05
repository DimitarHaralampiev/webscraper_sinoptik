import csv
from datetime import datetime

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
    high_temperature = Column(Float)
    low_temperature = Column(Float)
    wind = Column(String)
    humidity = Column(Integer)


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

    def import_weather_data_from_csv(self, csv_file: str):
        """
        Import weather data from a CSV file and store it in the database.

        Args:
            csv_file (str): Path to the CSV file containing weather data.
        """
        engine = create_engine(f'sqlite:///{self.database_name}')
        session = self.create_session(engine)

        try:
            with open(csv_file, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    try:
                        current_time = datetime.strptime(row['Current time'], '%Y-%m-%d %H:%M:%S')

                        weather = CurrentWeather(
                            town_name=row['Town'],
                            current_time=current_time,
                            current_temperature=float(row['Current Temp.']),
                            weather_condition=row['Condition'],
                            wind=row['Wind'],
                            humidity=int(row['Humidity'])
                        )
                        session.add(weather)
                    except ValueError:
                        print('Error importing data')

            session.commit()
        except FileNotFoundError:
            print(f'CSV file {csv_file} does not exist')
        finally:
            session.close()
