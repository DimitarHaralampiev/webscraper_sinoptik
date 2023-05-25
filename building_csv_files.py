import pandas as pd

from csv_helper import CSVHelper
from scraper_sinoptik import SinoptikScraper


def current_weather(town: str):
    """
    Retrieves and saves the current weather data for a given town.

    Args:
        town (str): The name of the town.
    """
    try:
        scraper = SinoptikScraper()
        entry = scraper.scrape_current_weather(town)
        if entry:
            weather_data = CSVHelper(entry, 'weather_data.csv')
            weather_data.write_csv()
    except ValueError:
        print('ERROR current weather')


def weather_ten_days(town: str, days: str):
    """
    Retrieves and saves the weather forecast data for the next ten days for a given town.

    Args:
        town (str): The name of the town.
        days (str): The number of days to retrieve the weather forecast for.
    """
    try:
        scraper = SinoptikScraper()
        forecast_weather = scraper.scrape_weather_ten_days(town, days)
        if forecast_weather:
            weather_data = CSVHelper(forecast_weather, 'forecast_weather_data.csv')
            weather_data.write_csv()
    except ValueError:
        print('ERROR forecast weather')


def combined_files_weather(town: str, period=None):
    weather_ten_days(town, period)
    current_weather(town)

    # Reading data for ten days
    weather_data_forecast = pd.read_csv('forecast_weather_data.csv')

    # Reading data for current weather
    weather_data_current = pd.read_csv('weather_data.csv')

    # Concat data from current and tend days weather
    combined_data = pd.concat([weather_data_current, weather_data_forecast], axis=1)

    # Create csv file with combined data
    combined_data.to_csv('combined_data_weather.csv', index=False)