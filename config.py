import configparser

config = configparser.ConfigParser()
config.read('config.cfg')

database_name = config.get('CONFIG', 'database_name')
base_url = config.get('CONFIG', 'base_url')
town_name = config.get('CONFIG', 'town_name')
period_weather = config.get('CONFIG', 'period_weather')
weather_data_csv = config.get('CONFIG', 'weather_data_csv')
forecast_weather_csv = config.get('CONFIG', 'forecast_weather_csv')