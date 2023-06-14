from csv_helper import CSVDataStore
from scraper_sinoptik import SinoptikScraper
from sql_helper import SQLiteDataStore


scraper = SinoptikScraper()

database_file = 'weather_data.db'
helper = SQLiteDataStore(database_file)


def retrieve_and_save_current_weather(town):
    """
    Retrieves and saves the current weather data for a given town.
    """
    try:
        entry = scraper.scrape_current_weather(town)
        if entry:
            weather_data = CSVDataStore(entry, 'weather_data.csv')
            weather_data.write_csv()
    except ValueError:
        print('ERROR retrieving or saving current weather data')


def retrieve_and_save_forecast_weather(town, period):
    """
    Retrieves and saves the weather forecast data for the next ten days for a given town.
    """
    try:
        forecast_weather = scraper.scrape_weather_ten_days(town, period)
        if forecast_weather:
            weather_data = CSVDataStore(forecast_weather, 'forecast_weather_data.csv')
            weather_data.write_csv()
    except ValueError:
        print('ERROR retrieving or saving forecast weather data')


def retrieve_and_save_to_database_current_weather(town):
    """
    Retrieve the current weather data for a given town and save it to the database.

    Args:
        town (str): The name of the town to retrieve weather data for.
    """
    try:
        current_weather_data = scraper.scrape_current_weather(town)
        for data in current_weather_data:
            helper.write(data)
    except ValueError as v:
        print(f'Error retrieving or saving current weather data: {str(v)}')


def retrieve_and_save_to_database_forecast_weather(town, period):
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


town = input('Please enter Town: ')
period = input('Please enter Period: ')

if __name__ == '__main__':

    retrieve_and_save_current_weather(town)
    retrieve_and_save_forecast_weather(town, period)

    helper.create_tables()

    retrieve_and_save_to_database_current_weather(town)
    retrieve_and_save_to_database_forecast_weather(town, period)




