import re
from datetime import datetime

import requests

from bs4 import BeautifulSoup


class SinoptikScraper:
    """
        A class for scraping weather data from sinoptik.bg.
    """
    def __init__(self, base_url):
        self.base_url = base_url

    def scrape_current_weather(self, town: str):
        """
        Scrape the current weather data for a given town.

        Returns:
            list: A list containing the scraped current weather data.
        """
        try:

            url = self.base_url + town

            soup = BeautifulSoup(requests.get(url).content, 'html.parser')

            try:

                current_weather_temp = soup.find('span', class_='wfCurrentTemp').text.strip()
                current_weather_feel = soup.find('span', class_='wfCurrentFeelTemp').text.strip()
                current_weather_conditional = soup.find('strong').text.strip()
                div_wind = soup.find('div', class_='wfCurrentWindWrapper')
                wind = div_wind.find('span', class_='wfCurrentWind windImgNW').text.strip()
                div_humidity = soup.find_all('div', class_='wfCurrentWrapper')

                humidity = ''

                for div in div_humidity:
                    heading_name = div.find('span', class_='wfCurrentHeading').text.title()
                    if heading_name == 'Humidity:':
                        humidity = div.find('span', class_='wfCurrentValue').text.strip()

                current_time = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

                return {
                    'Town': town.split('-')[0],
                    'Current time': current_time,
                    'Current Temp.': current_weather_temp.replace('°C', ''),
                    'Condition': current_weather_conditional,
                    'Wind': wind,
                    'Humidity': humidity.replace('%', '')
                }
            except ValueError as v:
                print(f'Error retrieving current weather data {str(v)}')
        except ValueError as v:
            print(f'ERROR retrieving current weather URL {str(v)}')

    def scrape_weather_ten_days(self, town: str, period: str):
        """
        Scrape the weather data for the next ten days for a given town.

        Returns:
            list: A list containing the scraped weather data for the next ten days.
        """
        weather_data_forecast = []

        try:

            url = self.base_url + town + '/' + period

            soup_ten_days = BeautifulSoup(requests.get(url).content, 'html.parser')

            ten_days_weather = soup_ten_days.find('div', class_='wf10dayRightContent')

            days = ten_days_weather.find_all('a')

            for day_info in days:
                if day_info.has_attr('class'):
                    try:

                        forecast_day = day_info.find('span', class_='wf10dayRightDay').text.strip()
                        forecast_date = day_info.find('span', class_='wf10dayRightDate').text.strip()
                        high_temp = day_info.find('span', class_='wf10dayRightTemp').text.strip()
                        low_temp = day_info.find('span', class_='wf10dayRightTempLow').text.strip()
                        wind = day_info.find('span', class_='wf10dayRightWind').text.strip()
                        humidity = day_info.find('span', class_='wf10dayRighValue wf10dayRightRainValue').text.strip()

                        pattern = r'(\d+) m/s'

                        match = re.search(pattern, wind)
                        if match:
                            wind = match.group(1)

                        formatting_forecast_date = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

                        weather_data_forecast.append({
                            'Town': town.split('-')[0],
                            'Forecast Day': forecast_day,
                            'Current time': formatting_forecast_date,
                            'Date': forecast_date,
                            'High temp': high_temp.replace('°', ''),
                            'Low temp': low_temp.replace('°', ''),
                            'Wind': wind,
                            'Humidity': humidity.replace('%', ''),
                        })
                    except ValueError as v:
                        print(f'ERROR retrieving forecast weather data {str(v)}')
        except ValueError as v:
            print(f'ERROR retrieving forecast weather URL {str(v)}')

        return weather_data_forecast


