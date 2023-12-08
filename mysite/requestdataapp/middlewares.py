import time
from django.http import HttpRequest, HttpResponse

def set_useragent_on_request_middleware(get_response):

    print("initial call")
    def middleware(request: HttpRequest):
        request.user_agent = request.META["HTTP_USER_AGENT"]
        response = get_response(request)

        return response

    return middleware


class CountRequestsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests_count = 0
        self.responses_count = 0
        self.exceptions_count = 0

    def __call__(self, request: HttpRequest):
        self.requests_count += 1
        response = self.get_response(request)
        self.responses_count += 1
        return response
    
    def process_exception(self, request: HttpRequest, exception: Exception):
        self.exceptions_count += 1


class IpCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.ip_time = dict()

    def __call__(self, request: HttpRequest):
        request.ip_address = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', ''))
        try:
            if request.ip_address in self.ip_time:
                now = time.time()
                if  now - self.ip_time[request.ip_address] < 1.00:
                    raise Exception("Quick request.")
        except Exception as es:
            return HttpResponse(f"ERROR: {es}")
        else:
            self.ip_time[request.ip_address] = time.time()
            response = self.get_response(request)
            return response