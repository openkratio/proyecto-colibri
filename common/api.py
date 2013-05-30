from tastypie.http import HttpResponse, HttpMethodNotAllowed
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.resources import Resource

#code from:
#http://codeispoetry.me/index.php/make-your-django-tastypie-api-cross-domain/

__author__ = '@danigosa'

class BaseCorsResource(Resource):
    """
    Class implementing CORS
    """

    def create_response(self, *args, **kwargs):
        response = super(BaseCorsResource, self).create_response(*args, **kwargs)
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Headers'] = 'Content-Type'
        return response

    def method_check(self, request, allowed=None):
        if allowed is None:
            allowed = []

        request_method = request.method.lower()
        allows = ','.join(map(str.upper, allowed))

        if request_method == 'options':
            response = HttpResponse(allows)
            response['Access-Control-Allow-Origin'] = '*'
            response['Access-Control-Allow-Headers'] = 'Content-Type'
            response['Allow'] = allows
            raise ImmediateHttpResponse(response=response)

        if not request_method in allowed:
            response = HttpMethodNotAllowed(allows)
            response['Allow'] = allows
            raise ImmediateHttpResponse(response=response)

        return request_method
