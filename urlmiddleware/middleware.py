from inspect import isclass, isfunction
from django.core.exceptions import ImproperlyConfigured
from django.utils.datastructures import SortedDict
from django.utils.functional import memoize

from urlmiddleware.base import MiddlewareResolver404
from urlmiddleware.urlresolvers import resolve

_match_cache = SortedDict()


def matched_middleware(path):
    return resolve(path)
matched_middleware = memoize(matched_middleware, _match_cache, 1)


class URLMiddleware(object):
    """
    To install urlmiddleware, one global middleware class needs to be
    added so it can then act as an entry point and match other middleware
    classes.
    """

    def get_matched_middleware(self, path):

        middleware_instances = []

        try:
            middleware_matches = matched_middleware(path)
        except MiddlewareResolver404:
            return []

        for middleware_class in middleware_matches:
            if not (isclass(middleware_class) or isfunction(middleware_class) \
                    or callable(middleware_class)):
                raise ImproperlyConfigured("%s is expected to be a callable that accepts no arguements." % middleware_class)
            try:
                middleware_instances.append(middleware_class())
            except TypeError:
                raise ImproperlyConfigured("%s is expected to be a callable that accepts no arguements." % middleware_class)

        return middleware_instances

    def process_request(self, request):
        matched_middleware = self.get_matched_middleware(request.path)
        for middleware in matched_middleware:
            if hasattr(middleware, 'process_request'):
                response = middleware.process_request(request)
                if response:
                    return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        matched_middleware = self.get_matched_middleware(request.path)
        for middleware in matched_middleware:
            if hasattr(middleware, 'process_view'):
                response = middleware.process_view(request, view_func, view_args, view_kwargs)
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

    def process_exception(self, request, exception):
        matched_middleware = self.get_matched_middleware(request.path)
        for middleware in matched_middleware:
            if hasattr(middleware, 'process_exception'):
                response = middleware.process_exception(request, exception)
                if response:
                    return response
