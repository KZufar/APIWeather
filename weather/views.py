from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import WeatherSerializer
from .services import WeatherService


class GetWeatherView(APIView):

    @staticmethod
    def get(request):
        serializer = WeatherSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        city_name = serializer.validated_data['city']

        weather_service = WeatherService()
        weather_data = weather_service.get_weather_data(city_name)

        return Response({
            'temperature': weather_data.temperature,
            'pressure': weather_data.pressure,
            'wind_speed': weather_data.wind_speed
        })
