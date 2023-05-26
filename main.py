from building_csv_files import BuildingCSVFilesForWeather

town = input('Please enter Town: ')
period = input('Please enter Period: ')


if __name__ == '__main__':
    weather_data = BuildingCSVFilesForWeather(town, period)
    weather_data.generate_combined_weather_csv()


