from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin


class ServerErrorJump(MiddlewareMixin):

    def __call__(self, request):
        response = super().__call__(request)

        response = self.process_exception(request, response)
        return response

    def process_exception(self, request, response):
        if response.status_code >= 500:
            response = HttpResponse('ErrorResponseJump : status_code >= 500')
        return response

