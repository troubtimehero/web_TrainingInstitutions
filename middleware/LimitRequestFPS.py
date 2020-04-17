from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin


class LimitRequestFPS(MiddlewareMixin):

    def process_request(self, request):
        ip = request.META.get('REMOTE_ADDR')

        # if ip == '127.0.0.1':
        #     return HttpResponse(ip)
        pass

