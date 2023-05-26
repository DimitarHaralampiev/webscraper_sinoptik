import pandas as pd

from csv_helper import CSVHelper
from scraper_sinoptik import SinoptikScraper


class BuildingCSVFilesForWeather:

    def __init__(self, town: str, period=None):
        self.town = town
        self.period = period

    def retrieve_and_save_current_weather(self):
        """
        Retrieves and saves the current weather data for a given town.
        """
        try:
            scrape = SinoptikScraper()
            entry = scrape.scrape_current_weather(self.town)
            if entry:
                weather_data = CSVHelper(entry, 'weather_data.csv')
                weather_data.write_csv()
        except ValueError:
            print('ERROR retrieving or saving current weather data')

    def retrieve_and_save_forecast_weather(self):
        """
        Retrieves and saves the weather forecast data for the next ten days for a given town.
        """
        try:
            scrape = SinoptikScraper()
            forecast_weather = scrape.scrape_weather_ten_days(self.town, self.period)
            if forecast_weather:
                weather_data = CSVHelper(forecast_weather, 'forecast_weather_data.csv')
                weather_data.write_csv()
        except ValueError:
            print('ERROR retrieving or saving forecast weather data')

    def generate_combined_weather_csv(self):
        """
        Combines the current weather and forecast weather data into a single CSV file.

        Retrieves the weather forecast data for the next ten days and the current weather data for a given town.
        Then, combines the data into a single DataFrame and saves it as a CSV file.
        """
        self.retrieve_and_save_forecast_weather()
        self.retrieve_and_save_current_weather()

        weather_data_forecast = pd.read_csv('forecast_weather_data.csv')

        weather_data_current = pd.read_csv('weather_data.csv')

        combined_data = pd.concat([weather_data_current, weather_data_forecast], axis=1)

        combined_data.to_csv('combined_data_weather.csv', index=False)