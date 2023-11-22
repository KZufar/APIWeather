from django.test import TestCase, Client
from rest_framework.exceptions import NotFound
from rest_framework.test import APIRequestFactory
from rest_framework import status
from django.core.cache import cache
from django.urls import reverse
from unittest.mock import patch

from .models import APIRequestLog
from .services import WeatherData
from .views import GetWeatherView, WeatherService


class GetWeatherViewTests(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.test_api_response = {
            "fact": {
                "temp": -10,
                "pressure_mm": 760,
                "wind_speed": 7
            }
        }

    @patch('requests.get')
    def test_get_weather_view(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.test_api_response

        with patch.object(WeatherService, 'get_coordinates', return_value=(40.7128, -74.0060)):
            url = reverse('get_weather')
            request = self.factory.get(url, {'city': 'Казань'})
            response = GetWeatherView.as_view()(request)

            self.assertEqual(response.status_code, status.HTTP_200_OK)

            expected_data = {
                'temperature': '-10 °C',
                'pressure': '760 мм рт. ст.',
                'wind_speed': '7 м/с'
            }
            self.assertEqual(response.data, expected_data)

            cache_key = 'weather:Казань'
            cached_weather_data = cache.get(cache_key)
            self.assertIsNotNone(cached_weather_data)
            self.assertEqual(cached_weather_data, WeatherData('-10 °C', '760 мм рт. ст.', '7 м/с'))

    @patch('requests.get')
    def test_invalid_city_name(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.test_api_response

        with patch.object(WeatherService, 'get_coordinates', side_effect=NotFound):
            url = reverse('get_weather')
            request = self.factory.get(url, {'city': 'Казан'})
            response = GetWeatherView.as_view()(request)

            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class LoggingMiddlewareTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_logging_middleware(self):
        params = {'city': 'Казань'}
        response = self.client.get('/weather/', data=params)

        self.assertEqual(response.status_code, 200)

        api_request_log = APIRequestLog.objects.last()

        self.assertIsNotNone(api_request_log)
        self.assertEqual(api_request_log.remote_addr, '127.0.0.1')
        self.assertEqual(api_request_log.path, '/weather/')
        self.assertEqual(api_request_log.query_params, str(params))
        self.assertEqual(api_request_log.request_method, 'GET')
        self.assertEqual(api_request_log.status_code, 200)
        self.assertEqual(api_request_log.response, str(response.data))

    def test_admin_requests_not_logged(self):
        self.client.get('/admin/')

        api_request_log = APIRequestLog.objects.last()
        self.assertIsNone(api_request_log)
