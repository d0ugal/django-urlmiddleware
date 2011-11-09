from django.core.exceptions import ImproperlyConfigured

from urlmiddleware.urlresolvers import MiddlewareRegexURLResolver, MiddlewareRegexURLPattern

__all__ = ['mpatterns', 'middleware', ]


def mpatterns(prefix, *args):
    pattern_list = []
    for t in args:
        if isinstance(t, (list, tuple)):
            t = middleware(prefix=prefix, *t)
        elif isinstance(t, MiddlewareRegexURLPattern):
            t.add_prefix(prefix)
        pattern_list.append(t)
    return pattern_list


def middleware(regex, view, kwargs=None, name=None, prefix=''):
    if isinstance(view, (list, tuple)):
        # For include(...) processing.
        urlconf_module, app_name, namespace = view
        return MiddlewareRegexURLResolver(regex, urlconf_module, kwargs, app_name=app_name, namespace=namespace)
    else:
        if isinstance(view, basestring):
            if not view:
                raise ImproperlyConfigured('Empty URL pattern view name not permitted (for pattern %r)' % regex)
            if prefix:
                view = prefix + '.' + view
        return MiddlewareRegexURLPattern(regex, view, kwargs, name)
