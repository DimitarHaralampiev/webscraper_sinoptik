from building_csv_files import combined_files_weather

town = input('Please enter Town: ')
period = input('Please enter Period: ')

if __name__ == '__main__':
    combined_files_weather(town, period)

