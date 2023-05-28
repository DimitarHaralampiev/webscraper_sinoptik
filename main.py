from building_csv_files import BuildingCSVFilesForWeather

town = input('Please enter Town: ')
period = input('Please enter Period: ')


if __name__ == '__main__':
    weather_data = BuildingCSVFilesForWeather(town, period)
    weather_data.retrieve_and_save_current_weather()
    weather_data.retrieve_and_save_forecast_weather()


