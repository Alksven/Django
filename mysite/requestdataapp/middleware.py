from django.http import HttpRequest


def set_useragent_on_request_middleware(get_response):
    def middleware(request: HttpRequest):
        request.user_agent = request.META["HTTP_USER_AGENT"]
        response = get_response(request)
        return response

    return middleware


class CountRequestsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.request_count = 0
        self.responses_count = 0
        self.exceptions_count = 0

    def __call__(self, request: HttpRequest):
        self.request_count += 1
        response = self.get_response(request)
        self.responses_count += 1
        return response

    def process_exceptions(self, request: HttpRequest, exception: Exception):
        self.exceptions_count += 1