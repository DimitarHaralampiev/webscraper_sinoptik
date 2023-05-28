from datetime import datetime

import requests

from bs4 import BeautifulSoup


class SinoptikScraper:
    """
        A class for scraping weather data from sinoptik.bg.
    """

    @staticmethod
    def remove_units(value: str):
        """
        Remove units (such as degrees Celsius, percentage, and degrees) from the given value.

        Args:
            value (str): The value containing units.

        Returns:
            str: The value with units removed.
        """
        return value.replace('°C', '').replace('%', '').replace('°', '')

    @staticmethod
    def __get_sinoptik_base_url() -> str:
        """
        Get the base URL for scraping weather data from Sinoptik.

        Returns:
            str: The base URL for Sinoptik weather data.
        """
        return f'https://weather.sinoptik.bg/'

    def scrape_current_weather(self, town: str):
        """
        Scrape the current weather data for a given town.

        Returns:
            list: A list containing the scraped current weather data.
        """
        try:

            url = self.__get_sinoptik_base_url() + town

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

                current_time = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

                return [{
                    'Town': town.split('-')[0],
                    'Current time': current_time,
                    'Current Temp.': self.remove_units(current_weather_temp),
                    'Current weather feel': self.remove_units(current_weather_feel.split(':')[1]),
                    'Condition': current_weather_conditional,
                    'Wind': wind,
                    'Humidity': self.remove_units(humidity)
                }]
            except ValueError:
                print('Error retrieving current weather data')
        except ValueError:
            print('ERROR retrieving current weather URL')

    def scrape_weather_ten_days(self, town: str, period: str):
        """
        Scrape the weather data for the next ten days for a given town.

        Returns:
            list: A list containing the scraped weather data for the next ten days.
        """
        weather_data_forecast = []

        try:

            url = self.__get_sinoptik_base_url() + town + '/' + period

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

                        humidity = humidity.replace('%', '')

                        formatting_forecast_date = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

                        weather_data_forecast.append({
                            'Town': town.split('-')[0],
                            'Forecast Day': forecast_day,
                            'Current time': formatting_forecast_date,
                            'Date': forecast_date,
                            'High temp': self.remove_units(high_temp),
                            'Low temp': self.remove_units(low_temp),
                            'Wind': wind,
                            'Humidity': self.remove_units(humidity),
                        })
                    except ValueError:
                        print('ERROR retrieving forecast weather data')
        except ValueError:
            print('ERROR retrieving forecast weather URL')

        return weather_data_forecast


