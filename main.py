from config import database_name, base_url, town_name, period_weather, weather_data_csv, forecast_weather_csv
from csv_data_store import CSVDataStore
from scraper_sinoptik import SinoptikScraper
from sql_data_store import SQLiteDataStore


scraper = SinoptikScraper(base_url)

helper = SQLiteDataStore(database_name)


def retrieve_and_save_current_weather(town: str):
    """
    Retrieves and saves the current weather data for a given town.
    """
    try:
        entry = scraper.scrape_current_weather(town)
        if entry:
            weather_data = CSVDataStore(weather_data_csv)
            weather_data.write([entry])
    except ValueError:
        print('ERROR retrieving or saving current weather data')


def retrieve_and_save_forecast_weather(town: str, period: str):
    """
    Retrieves and saves the weather forecast data for the next ten days for a given town.
    """
    try:
        forecast_weather = scraper.scrape_weather_ten_days(town, period)
        if forecast_weather:
            weather_data = CSVDataStore(forecast_weather_csv)
            weather_data.write(forecast_weather)
    except ValueError:
        print('ERROR retrieving or saving forecast weather data')


def retrieve_and_save_to_database_current_weather(town: str):
    """
    Retrieve the current weather data for a given town and save it to the database.

    Args:
        town (str): The name of the town to retrieve weather data for.
    """
    try:
        current_weather_data = scraper.scrape_current_weather(town)
        # for data in current_weather_data:
        helper.write(current_weather_data)
    except ValueError as v:
        print(f'Error retrieving or saving current weather data: {str(v)}')


def retrieve_and_save_to_database_forecast_weather(town: str, period: str):
    """
    Retrieve the current weather data for a given town and save it to the database.

    Args:
        town (str): The name of the town to retrieve weather data for.
    """
    try:
        forecast_weather_data = scraper.scrape_weather_ten_days(town, period)
        for data in forecast_weather_data:
            helper.write(data)
    except ValueError as v:
        print(f'Error retrieving or saving forecast weather data: {str(v)}')


if __name__ == '__main__':

    retrieve_and_save_current_weather(town_name)
    retrieve_and_save_forecast_weather(town_name, period_weather)

    helper.create_tables()

    retrieve_and_save_to_database_current_weather(town_name)
    retrieve_and_save_to_database_forecast_weather(town_name, period_weather)






