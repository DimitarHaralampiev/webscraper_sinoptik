from base_data_store import BaseDataStore
from config import database_name, base_url, town_name, period_weather, weather_data_csv, forecast_weather_csv
from scraper_sinoptik import SinoptikScraper
from sql_data_store import SQLiteDataStore


scraper = SinoptikScraper(base_url)

helper = SQLiteDataStore(database_name)


def retrieve_and_save_current_weather(town: str, data_store: BaseDataStore):
    """
    Retrieves and saves the current weather data for a given town.

    Args:
        town (str): The name of the town to retrieve weather data for.
        data_store (BaseDataStore): The data store object to write the data to.
    """
    try:
        entry = scraper.scrape_current_weather(town)
        if entry:
            data_store.write(entry)
    except ValueError:
        print('ERROR retrieving or saving current weather data')


def retrieve_and_save_forecast_weather(town: str, period: str, data_store: BaseDataStore):
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
            for data in forecast_weather:
                data_store.write(data)
    except ValueError:
        print('ERROR retrieving or saving forecast weather data')


if __name__ == '__main__':

    retrieve_and_save_current_weather(town_name)
    retrieve_and_save_forecast_weather(town_name, period_weather)

    helper.create_tables()







