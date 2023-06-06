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

    def import_weather_data_from_csv(self, csv_file: str):
        """
        Import weather data from a CSV file and store it in the database.

        Args:
            csv_file (str): Path to the CSV file containing weather data.
        """
        engine = create_engine(f'sqlite:///{self.database_name}')
        session = self.__create_session(engine)

        try:
            with open(csv_file, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    try:
                        formatted_current_time = datetime.now().strptime(row['Current time'],
                                                                         '%Y-%m-%d %H:%M:%S')

                        weather = current_weather(
                            town_name=row['Town'],
                            current_time=formatted_current_time,
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

    def import_forecast_weather_from_csv(self, csv_file: str):
        """
        Import forecast weather data from a CSV file and store it in the database.

        Args:
            csv_file (str): Path to the CSV file containing forecast weather data.
        """
        engine = create_engine(f'sqlite:///{self.database_name}')
        session = self.__create_session(engine)

        try:
            with open(csv_file, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    try:
                        formatted_forecast_current_time = datetime.now().strptime(row['Current time'],
                                                                                  '%Y-%m-%d %H:%M:%S')

                        forecast = forecast_weather(
                            town_name=row['Town'],
                            forecast_day=row['Forecast Day'],
                            current_time=formatted_forecast_current_time,
                            forecast_date=row['Date'],
                            high_temperature=float(row['High temp']),
                            low_temperature=float(row['Low temp']),
                            wind=row['Wind'],
                            humidity=int(row['Humidity'])
                        )
                        session.add(forecast)
                    except ValueError:
                        print('Error importing forecast data')

                session.commit()
        except FileNotFoundError:
            print(f'Forecast CSV file {csv_file} does not exist')
        finally:
            session.close()
