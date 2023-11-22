import requests

from dataclasses import dataclass
from typing import Tuple

from django.conf import settings
from django.core.cache import cache
from rest_framework.exceptions import NotFound


@dataclass
class WeatherData:
    temperature: str
    pressure: str
    wind_speed: str


class WeatherService:
    API_KEY = settings.YANDEX_WEATHER_API_KEY
    PATH_TO_CITY_COORDINATES = 'Координаты городов.txt'

    def get_coordinates(self, city_name: str) -> Tuple[float, float]:
        with open(self.PATH_TO_CITY_COORDINATES, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split(' — ')
                if len(parts) != 2:
                    continue
                name, coordinates = parts
                if name == city_name:
                    lat, lon = map(float, coordinates.split(', '))
                    return lat, lon

        raise NotFound('Проверьте название города и попробуйте еще раз!')

    def get_weather_data(self, city_name) -> WeatherData:
        cache_key = f'weather:{city_name}'
        cached_weather_data = cache.get(cache_key)

        if cached_weather_data:
            return cached_weather_data

        lat, lon = self.get_coordinates(city_name)

        params = {
            'lat': lat,
            'lon': lon,
            'lang': 'ru_RU',
            'limit': 7,
            'hours': True,
            'extra': False
        }

        print('Получение погоды от Яндекса...')

        response = requests.get(
            url='https://api.weather.yandex.ru/v2/forecast',
            params=params,
            headers={'X-Yandex-API-Key': self.API_KEY}
        )

        if response.status_code == 200:
            data = response.json()
            temperature = f'{data["fact"]["temp"]} °C'
            pressure = f'{data["fact"]["pressure_mm"]} мм рт. ст.'
            wind_speed = f'{data["fact"]["wind_speed"]} м/с'
            weather_data = WeatherData(temperature, pressure, wind_speed)

            cache.set(cache_key, weather_data, timeout=settings.CACHE_TIMEOUT_FOR_API_YANDEX)

            return weather_data
        else:
            raise Exception('Проверьте X-Yandex-API-Key и попробуйте еще раз!')
