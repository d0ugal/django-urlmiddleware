from django.utils.functional import memoize

from urlmiddleware.urlresolvers import resolve

_match_cache = {}


def get_matched_middleware(path):
    return resolve(path)
memoize(get_matched_middleware, _match_cache, 1)


class UrlMiddlewareMiddleware(object):
    """
    To install urlmiddleware, one global middleware class needs to be
    added so it can then act as an entry point and match other middleware
    classes.
    """

    def __init__(self):
        self._cache = {}

    def get_matched_middleware(self, path):
        return get_matched_middleware(path)

    def process_request(self, request, *args, **kwargs):
        matched_middleware = self.get_matched_middleware(request.path)
        for middleware in matched_middleware:
            if hasattr(middleware, 'process_request'):
                response = middleware.process_request(request, *args, **kwargs)
                if response:
                    return response

    def process_view(self, request, *args, **kwargs):
        matched_middleware = self.get_matched_middleware(request.path)
        for middleware in matched_middleware:
            if hasattr(middleware, 'process_view'):
                response = middleware.process_view(request, *args, **kwargs)
                if response:
                    return response

    def process_template_response(self, request, response):
        matched_middleware = self.get_matched_middleware(request.path)
        for middleware in matched_middleware:
            if hasattr(middleware, 'process_template_response'):
                response = middleware.process_template_response(request, response)
        return response

    def process_response(self, request, response):
        matched_middleware = self.get_matched_middleware(request.path)
        for middleware in matched_middleware:
            if hasattr(middleware, 'process_response'):
                response = middleware.process_response(request, response)
        return response

    def process_exception(self, request, *args, **kwargs):
        matched_middleware = self.get_matched_middleware(request.path)
        for middleware in matched_middleware:
            if hasattr(middleware, 'process_exception'):
                response = middleware.process_exception(request, *args, **kwargs)
                if response:
                    return response
