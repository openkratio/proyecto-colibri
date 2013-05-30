# XHR CrossDomain Middleware by robtotheb
# https://gist.github.com/1164697
# improvements:
# https://gist.github.com/5657491

from django import http

XS_SHARING_ALLOWED_ORIGINS = '*'
XS_SHARING_ALLOWED_METHODS = 'POST, GET, OPTIONS, PUT, DELETE'
XS_SHARING_ALLOWED_HEADERS = 'Accept, Accept-Charset, Accept-Encoding, ' \
    'Accept-Language, Connection, Content-Type, Authorization, ' \
    'Cache-Control, Referer, User-Agent, Origin'
XS_SHARING_ALLOWED_CREDENTIALS = 'true'


class XsSharing(object):
    """
        This middleware allows cross-domain XHR
        using the html5 postMessage API.
        Access-Control-Allow-Origin: http://foo.example
        Access-Control-Allow-Methods: POST, GET, OPTIONS, PUT, DELETE
    """
    def process_request(self, request):
        if 'HTTP_ACCESS_CONTROL_REQUEST_METHOD' in request.META:
            response = http.HttpResponse()
            response['Access-Control-Allow-Origin'] = XS_SHARING_ALLOWED_ORIGINS
            response['Access-Control-Allow-Methods'] = XS_SHARING_ALLOWED_METHODS
            response['Access-Control-Allow-Headers'] = XS_SHARING_ALLOWED_HEADERS
            response['Access-Control-Allow-Credentials'] = XS_SHARING_ALLOWED_CREDENTIALS
            return response
        return None

    def process_response(self, request, response):
        # Avoid unnecessary work
        if response.has_header('Access-Control-Allow-Origin'):
            return response
        response['Access-Control-Allow-Origin'] = XS_SHARING_ALLOWED_ORIGINS
        response['Access-Control-Allow-Methods'] = XS_SHARING_ALLOWED_METHODS
        response['Access-Control-Allow-Headers'] = XS_SHARING_ALLOWED_HEADERS
        response['Access-Control-Allow-Credentials'] = XS_SHARING_ALLOWED_CREDENTIALS
        return response
