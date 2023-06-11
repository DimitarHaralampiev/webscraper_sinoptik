import csv
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from base_data_store import BaseDataStore
from models.current_weather import Base, current_weather
from models.forecast_weather import Base, forecast_weather


class SQLiteDataStore(BaseDataStore):
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

    def write(self, data):
        """
        Write the data to the SQLite database.

        Args:
            data: The data to be written.
        """
        engine = create_engine(f'sqlite:///{self.database_name}')
        session = self.__create_session(engine)

        try:
            if isinstance(data, dict):
                formatted_current_time = datetime.now().strptime('Current time',
                                                                 '%Y-%m-%d %H:%M:%S')

                current_weather_data = current_weather(
                    town_name=data['Town'],
                    current_time=formatted_current_time,
                    current_temperature=data['Current Temp.'],
                    weather_condition=data['Condition'],
                    wind=data['Wind'],
                    humidity=['Humidity']
                )
                session.add(current_weather_data)
            elif isinstance(data, list):
                for item in data:
                    formatted_current_time = datetime.now().strptime('Current time',
                                                                     '%Y-%m-%d %H:%M:%S')

                    forecast_weather_data = forecast_weather(
                        townn_name=item['Town'],
                        forecast_day=item['Forecast Day'],
                        current_time=formatted_current_time,
                        forecast_data=item['Date'],
                        high_temperature=item['High temp'],
                        low_temperature=item['Low temp'],
                        wind=item['Wind'],
                        humidity=item['Humidity']
                    )
                    session.add(forecast_weather_data)

            session.commit()
        except ValueError as v:
            print(f'Error writing data to the database: {str(v)}')
        finally:
            session.close()

    def get(self):
        """
        Retrieve the data from the SQLite database.

        Returns:
            The retrieved data.
        """
        engine = create_engine(f'sqlite:///{self.database_name}')
        session = self.__create_session(engine)

        try:
            current_weather_data = session.query(current_weather).all()
            forecast_weather_data = session.query(forecast_weather).all()

            current_data = []
            for weather in current_weather_data:
                current_data.append({
                    'Town': weather.town_name,
                    'Current time': weather.current_time,
                    'Current Temp.': weather.current_temperature,
                    'Condition': weather.weather_condition,
                    'Wind': weather.wind,
                    'Humidity': weather.humidity
                })

            forecast_data = []
            for weather in forecast_weather_data:
                forecast_data.append({
                    'Town': weather.town_name,
                    'Forecast Day': weather.forecast_day,
                    'Current time': weather.current_time,
                    'Date': weather.forecast_date,
                    'High Temp.': weather.high_temperature,
                    'Low Temp.': weather.low_temperature,
                    'Wind': weather.wind,
                    'Humidity': weather.humidity
                })

            return {
                'current_weather': current_data,
                'forecast_weather': forecast_data
            }
        except ValueError as v:
            print(f'Error retrieving data from the database: {str(v)}')
        finally:
            session.close()


