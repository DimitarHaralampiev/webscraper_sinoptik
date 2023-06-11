from csv_helper import CSVHelper
from scraper_sinoptik import SinoptikScraper
from sql_helper import SQLHelper


def retrieve_and_save_current_weather(town):
    """
    Retrieves and saves the current weather data for a given town.
    """
    try:
        scrape = SinoptikScraper()
        entry = scrape.scrape_current_weather(town)
        if entry:
            weather_data = CSVHelper(entry, 'weather_data.csv')
            weather_data.write_csv()
    except ValueError:
        print('ERROR retrieving or saving current weather data')


def retrieve_and_save_forecast_weather(town, period):
    """
    Retrieves and saves the weather forecast data for the next ten days for a given town.
    """
    try:
        scrape = SinoptikScraper()
        forecast_weather = scrape.scrape_weather_ten_days(town, period)
        if forecast_weather:
            weather_data = CSVHelper(forecast_weather, 'forecast_weather_data.csv')
            weather_data.write_csv()
    except ValueError:
        print('ERROR retrieving or saving forecast weather data')


town = input('Please enter Town: ')
period = input('Please enter Period: ')

if __name__ == '__main__':

    retrieve_and_save_current_weather(town)
    retrieve_and_save_forecast_weather(town, period)

    database_file = 'weather_data.db'
    helper = SQLHelper(database_file)

    helper.create_tables()

    weather_csv_file = 'weather_data.csv'
    forecast_weather_csv_file = 'forecast_weather_data.csv'






