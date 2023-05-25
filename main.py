from building_csv_files import BuildingCSVFiles

town = input('Please enter Town: ')
period = input('Please enter Period: ')


if __name__ == '__main__':
    weather_data = BuildingCSVFiles(town, period)
    weather_data.combined_files_weather()


