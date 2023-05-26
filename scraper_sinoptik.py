from datetime import datetime

import requests

from bs4 import BeautifulSoup


class SinoptikScraper:
    """
        A class for scraping weather data from sinoptik.bg.
    """
    def __init__(self, town: str, period=None):
        self.town = town
        self.period = period

    def __get_sinoptik_base_url(self):
        return f'https://weather.sinoptik.bg/'

    def scrape_current_weather(self):
        """
        Scrape the current weather data for a given town.

        Returns:
            list: A list containing the scraped current weather data.
        """
        try:

            url = self.__get_sinoptik_base_url() + self.town

            soup = BeautifulSoup(requests.get(url).content, 'html.parser')

            try:

                current_weather_temp = soup.find('span', class_='wfCurrentTemp').text.strip()
                current_weather_feel = soup.find('span', class_='wfCurrentFeelTemp').text.strip()
                current_weather_conditional = soup.find('strong').text.strip()
                div_wind = soup.find('div', class_='wfCurrentWindWrapper')
                wind = div_wind.find('span', class_='wfCurrentWind windImgNE')
                div_humidity = soup.find_all('div', class_='wfCurrentWrapper')

                humidity = ''

                for div in div_humidity:
                    heading_name = div.find('span', class_='wfCurrentHeading').text.title()
                    if heading_name == 'Humidity:':
                        humidity = div.find('span', class_='wfCurrentValue').text.strip()

                current_day = str(datetime.now().today().day)
                current_time = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

                return [{
                    'Town': self.town.split('-')[0],
                    'Day': current_day,
                    'Current time': current_time,
                    'Current Temp.': current_weather_temp,
                    'Current weather feel': current_weather_feel,
                    'Condition': current_weather_conditional,
                    'Wind': wind,
                    'Humidity': humidity
                }]
            except ValueError:
                print('Error retrieving current weather data')
        except ValueError:
            print('ERROR retrieving current weather URL')

    def scrape_weather_ten_days(self):
        """
        Scrape the weather data for the next ten days for a given town.

        Returns:
            list: A list containing the scraped weather data for the next ten days.
        """
        weather_data_forecast = []

        try:

            url = self.__get_sinoptik_base_url() + self.town + '/' + self.period

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

                        formatting_forecast_date = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

                        weather_data_forecast.append({
                            'Town': self.town.split('-')[0],
                            'Day': forecast_day,
                            'Current time': formatting_forecast_date,
                            'Date': forecast_date,
                            'High temp': high_temp,
                            'Low temp': low_temp,
                            'Wind': wind,
                            'Humidity': humidity,
                        })
                    except ValueError:
                        print('ERROR retrieving forecast weather data')
        except ValueError:
            print('ERROR retrieving forecast weather URL')

        return weather_data_forecast


