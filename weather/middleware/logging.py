from django.utils import timezone

from weather.models import APIRequestLog


class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path_info.startswith('/admin/'):
            return self.get_response(request)

        request_date_time = timezone.now()

        response = self.get_response(request)

        APIRequestLog.objects.create(
            remote_addr=request.META.get('REMOTE_ADDR'),
            request_datetime=request_date_time,
            response_datetime=timezone.now(),
            path=request.path,
            query_params=request.GET.dict(),
            request_method=request.method,
            response=response.data if 'data' in response.__dict__ else response.content.decode('utf-8'),
            status_code=response.status_code,
        )

        return response
