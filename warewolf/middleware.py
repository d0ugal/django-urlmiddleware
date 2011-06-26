from threading import local

from django.core.urlresolvers import RegexURLResolver
from django.utils.functional import memoize

_resolver_cache = {}
_urlconfs = local()

class MiddlewareRegexURLResolver(RegexURLResolver):

    @property
    def url_patterns(self):
        patterns = getattr(self.urlconf_module, "middlewarepatterns", self.urlconf_module)
        try:
            iter(patterns)
        except TypeError:
            raise ImproperlyConfigured("The included urlconf %s doesn't have any patterns in it" % self.urlconf_name)
        return patterns

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

class WarewolfMiddleware(object):
	
	def __call__(self, *args, **kwargs):
		pass

	def process_request(self, request):

		print resolve(request.path)