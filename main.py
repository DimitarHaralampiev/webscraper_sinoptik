import argparse

from base_data_store import BaseDataStore
from config import database_name, base_url, town_name, period_weather, weather_data_csv, forecast_weather_csv
from csv_data_store import CSVDataStore
from scraper_sinoptik import SinoptikScraper
from sql_data_store import SQLiteDataStore


scraper = SinoptikScraper(base_url)

helper = SQLiteDataStore(database_name)

parser = argparse.ArgumentParser(description='Weather Data Scraper')

# Add the storage type argument
parser.add_argument('--store', choices=['csv', 'db'], default='db', help='Specify the storage type (csv or db)')
# Add the database name argument
parser.add_argument('--db_name', default=database_name, help='Specify the name or path of the database file')
# Add the CSV filenames argument
parser.add_argument('--weather-data-file', default=weather_data_csv, help='Name or path of the weather data file')
parser.add_argument('--forecast-data-file', default=forecast_weather_csv, help='Name or path of the forecast data file')

# Parse the arguments
args = parser.parse_args()


def retrieve_and_save_current_weather(town: str, save_type: str, data_store: BaseDataStore):
    """
    Retrieves and saves the current weather data for a given town.

    Args:
        town (str): The name of the town to retrieve weather data for.
        data_store (BaseDataStore): The data store object to write the data to.
    """
    try:
        entry = scraper.scrape_current_weather(town)
        if entry:
            if save_type == 'csv':
                data_store.write([entry])
            else:
                data_store.write(entry)
    except ValueError:
        print('ERROR retrieving or saving current weather data')


def retrieve_and_save_forecast_weather(town: str, period: str, save_type: str,  data_store: BaseDataStore):
    """
    Retrieves and saves the weather forecast data for the next ten days for a given town.

    Args:
        town (str): The name of the town to retrieve weather data for.
        period (str): The period for the weather forecast.
        data_store (BaseDataStore): The data store object to write the data to.
    """
    try:
        forecast_weather = scraper.scrape_weather_ten_days(town, period)
        if forecast_weather:
            if save_type == 'csv':
                data_store.write(forecast_weather)
            else:
                for data in forecast_weather:
                    data_store.write(data)
    except ValueError:
        print('ERROR retrieving or saving forecast weather data')


if __name__ == '__main__':

    if args.store == 'csv':
        # Use CSVDataStore for storage
        weather_data = CSVDataStore(args.weather_data_file)
        forecast_data = CSVDataStore(args.forecast_data_file)
        retrieve_and_save_current_weather(town_name, args.store, weather_data)
        retrieve_and_save_forecast_weather(town_name, period_weather, args.store, forecast_data)
    elif args.store == 'db':
        # Use SQLiteDataStore for storage
        data_store = SQLiteDataStore(args.db_name)
        data_store.create_tables()
        retrieve_and_save_current_weather(town_name, args.store, data_store)
        retrieve_and_save_forecast_weather(town_name, period_weather, args.store, data_store)
