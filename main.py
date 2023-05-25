from scraper_sinoptik import weather_ten_days, current_weather

import pandas as pd


if __name__ == '__main__':
    weather_ten_days('sofia-bulgaria-100727011', '10-days')
    current_weather('sofia-bulgaria-100727011')

    # Reading data for ten days
    weather_data_forecast = pd.read_csv('forecast_weather_data.csv')

    # Reading data for current weather
    weather_data_current = pd.read_csv('weather_data.csv')

    # Concat data from current and tend days weather
    combined_data = pd.concat([weather_data_current, weather_data_forecast], axis=1)

    # Create csv file with combined data
    combined_data.to_csv('combined_data_weather.csv', index=False)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/