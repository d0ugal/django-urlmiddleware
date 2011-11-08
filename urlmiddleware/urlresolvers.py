from threading import local

from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import RegexURLResolver, RegexURLPattern, ResolverMatch
from django.utils.encoding import smart_str
from django.utils.functional import memoize

from urlmiddleware.base import MiddlewareResolver404
from urlmiddleware.util.collections import OrderedSet

_resolver_cache = {}
_urlconfs = local()


class MiddlewareRegexURLPattern(RegexURLPattern):
    pass


class MiddlewareRegexURLResolver(RegexURLResolver):
    """
    This extends Django's RegexURLResolver to support picking up middleware
    from middlewarepatterns in urls.py files rather than urlpatterns and it
    also supports multiple matches rather than taking only the first.

    Much of this code is then taken from django.core.urlresolvers and tweaked
    slightly.
    """

    @property
    def url_patterns(self):
        patterns = getattr(self.urlconf_module, "middlewarepatterns", self.urlconf_module)
        try:
            iter(patterns)
        except TypeError:
            raise ImproperlyConfigured("The included urlconf %s doesn't have any middlewarepatterns in it" % self.urlconf_name)
        return patterns

    def resolve(self, path):
        tried = []
        found = OrderedSet()
        match = self.regex.search(path)
        if match:
            new_path = path[match.end():]
            for pattern in self.url_patterns:
                try:
                    sub_match = pattern.resolve(new_path)
                except MiddlewareResolver404, e:
                    sub_tried = e.args[0].get('tried')
                    if sub_tried is not None:
                        tried.extend([[pattern] + t for t in sub_tried])
                    else:
                        tried.append([pattern])
                else:
                    if sub_match:
                        sub_match_dict = dict([(smart_str(k), v) for k, v in match.groupdict().items()])
                        sub_match_dict.update(self.default_kwargs)
                        for k, v in sub_match.kwargs.iteritems():
                            sub_match_dict[smart_str(k)] = v
                        middleware = ResolverMatch(sub_match.func, sub_match.args, sub_match_dict, sub_match.url_name, self.app_name or sub_match.app_name, [self.namespace] + sub_match.namespaces)
                        found.add(middleware.func)
                    tried.append([pattern])
            if len(found) == 0:
                raise MiddlewareResolver404({'tried': tried, 'path': new_path})
        if len(found) == 0:
            raise MiddlewareResolver404({'path': path})
        return list(found)


def get_resolver(urlconf):
    if urlconf is None:
        from django.conf import settings
        urlconf = settings.ROOT_URLCONF
    return MiddlewareRegexURLResolver(r'^/', urlconf)
get_resolver = memoize(get_resolver, _resolver_cache, 1)


def resolve(path, urlconf=None):
    if urlconf is None:
        urlconf = get_urlconf()
    return get_resolver(urlconf).resolve(path)


def get_urlconf(default=None):
    """
    Returns the root URLconf to use for the current thread if it has been
    changed from the default one.
    """
    return getattr(_urlconfs, "value", default)
