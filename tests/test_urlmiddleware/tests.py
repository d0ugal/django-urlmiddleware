from django.test import TestCase
from django.test.client import Client
from django.test.client import RequestFactory

from mock import patch


class ResolverTestCase(TestCase):

    def test_resolve_api(self):

        from urlmiddleware.urlresolvers import resolve
        from test_urlmiddleware.middleware import NoOpMiddleWare

        middleware = resolve('/')

        self.assertEquals([NoOpMiddleWare, ], middleware)

    def test_resolve_multiple(self):

        from urlmiddleware.urlresolvers import resolve
        from test_urlmiddleware.middleware import NoOpMiddleWare, NoOpMiddleWare2

        middleware = resolve('/sub/')

        self.assertEquals([NoOpMiddleWare, NoOpMiddleWare2, ], middleware)

    def test_dotted_middleware_path(self):

        from urlmiddleware.urlresolvers import resolve
        from test_urlmiddleware.middleware import NoOpMiddleWare3, NoOpMiddleWare4

        middleware = resolve('/dotted/')

        self.assertEquals([NoOpMiddleWare3, NoOpMiddleWare4, ], middleware)

    def test_duplicated_middleware(self):

        from urlmiddleware.urlresolvers import resolve
        from test_urlmiddleware.middleware import NoOpMiddleWare5

        middleware = resolve('/dupe/')

        self.assertEquals([NoOpMiddleWare5, ], middleware)

    def test_dotted_sub_path(self):

        from urlmiddleware.urlresolvers import resolve
        from test_urlmiddleware.middleware import NoOpMiddleWare6

        middleware = resolve('/dotted2/')

        self.assertEquals([NoOpMiddleWare6, ], middleware)

    def test_no_middleware_Action(self):

        c = Client()

        c.get('/')

    def test_middleware(self):

        from urlmiddleware import URLMiddleware

        URLMiddleware()


class MiddlewareTestCase(TestCase):

    def test_getting_matched(self):

        from urlmiddleware import URLMiddleware
        from test_urlmiddleware.middleware import NoOpMiddleWare

        m = URLMiddleware()
        middleware = m.get_matched_middleware("/")

        self.assertEquals(middleware[0].__class__, NoOpMiddleWare)

    def test_no_middleware_url(self):

        from urlmiddleware import URLMiddleware

        m = URLMiddleware()
        middleware = m.get_matched_middleware("/no_middleware/")

        self.assertEquals(middleware, [])


class MatchingCacheTestCase(TestCase):

    def test_match_cache(self):

        from urlmiddleware.middleware import _match_cache, URLMiddleware
        from test_urlmiddleware.middleware import NoOpMiddleWare

        keys = _match_cache.keys()[:] + [('/',), ]

        m = URLMiddleware()
        m.get_matched_middleware('/')

        self.assertEqual(_match_cache.keys(), keys)
        self.assertEqual(_match_cache[('/',)], [NoOpMiddleWare, ])


class MiddlewareHooksTestCase(TestCase):

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

    def test_process_request_no_op(self):

        from urlmiddleware import URLMiddleware

        class MyProcessRequestMiddleware(object):

            def process_request(self, request, *args, **kwargs):
                pass

        def mock_match(self, path):
            return [MyProcessRequestMiddleware(), ]

        request = self.factory.get('/foo/bar/')

        with patch.object(URLMiddleware, 'get_matched_middleware', mock_match):

            m = URLMiddleware()

            self.assertEquals(m.process_request(request), None)

    def test_process_request(self):

        from urlmiddleware import URLMiddleware

        class MyProcessRequestMiddleware(object):

            def process_request(self, request, *args, **kwargs):
                from django.http import HttpResponse
                return HttpResponse("New Process Request Response")

        def mock_match(self, path):
            return [MyProcessRequestMiddleware(), ]

        request = self.factory.get('/foo/bar/')

        with patch.object(URLMiddleware, 'get_matched_middleware', mock_match):

            m = URLMiddleware()

            expected_content = "New Process Request Response"
            self.assertEquals(m.process_request(request).content, expected_content)

    def test_process_view_no_op(self):

        from urlmiddleware import URLMiddleware

        class MyProcessViewMiddleware(object):

            def process_view(self, request, view, view_args, view_kwargs):
                pass

        def mock_match(self, path):
            return [MyProcessViewMiddleware(), ]

        request = self.factory.get('/foo/bar/')

        with patch.object(URLMiddleware, 'get_matched_middleware', mock_match):

            m = URLMiddleware()

            self.assertEquals(m.process_view(request, lambda x: None, [], {}), None)

    def test_process_view(self):

        from urlmiddleware import URLMiddleware

        class MyProcessViewMiddleware(object):

            def process_view(self, request, view, view_args, view_kwargs):
                from django.http import HttpResponse
                return HttpResponse("New Process View Response")

        def mock_match(self, path):
            return [MyProcessViewMiddleware(), ]

        request = self.factory.get('/foo/bar/')

        with patch.object(URLMiddleware, 'get_matched_middleware', mock_match):

            m = URLMiddleware()

            expected_content = "New Process View Response"
            self.assertEquals(m.process_view(request, lambda x: None, [], {}).content, expected_content)

    def test_process_template_resnpose_no_op(self):

        from django.template.response import TemplateResponse

        from urlmiddleware import URLMiddleware

        class MyTemplateResnponseViewMiddleware(object):

            def process_template_response(self, request, response):
                return response

        def mock_match(self, path):
            return [MyTemplateResnponseViewMiddleware(), ]

        request = self.factory.get('/foo/bar/')
        template_response = TemplateResponse(request, 'base.html')

        with patch.object(URLMiddleware, 'get_matched_middleware', mock_match):

            m = URLMiddleware()

            self.assertEquals(m.process_template_response(request, template_response), template_response)

    def test_process_template_resnpose(self):

        from django.template.response import TemplateResponse

        from urlmiddleware import URLMiddleware

        request = self.factory.get('/foo/bar/')
        template_response = TemplateResponse(request, 'base.html')
        new = TemplateResponse(request, 'base.html')

        class MyTemplateResnponseViewMiddleware(object):

            def process_template_response(self, request, response):
                return new

        def mock_match(self, path):
            return [MyTemplateResnponseViewMiddleware(), ]

        with patch.object(URLMiddleware, 'get_matched_middleware', mock_match):

            m = URLMiddleware()

            self.assertEquals(m.process_template_response(request, template_response), new)

    def test_process_response_no_op(self):

        from django.http import HttpResponse

        from urlmiddleware import URLMiddleware

        class MyTemplateResnponseViewMiddleware(object):

            def process_response(self, request, response):
                return response

        def mock_match(self, path):
            return [MyTemplateResnponseViewMiddleware(), ]

        request = self.factory.get('/foo/bar/')
        response = HttpResponse("Response")

        with patch.object(URLMiddleware, 'get_matched_middleware', mock_match):

            m = URLMiddleware()

            self.assertEquals(m.process_response(request, response), response)

    def test_process_response(self):

        from django.http import HttpResponse

        from urlmiddleware import URLMiddleware

        class MyTemplateResnponseViewMiddleware(object):

            def process_response(self, request, response):
                from django.http import HttpResponse
                return HttpResponse("New Response")

        def mock_match(self, path):
            return [MyTemplateResnponseViewMiddleware(), ]

        request = self.factory.get('/foo/bar/')
        response = HttpResponse("Response")

        with patch.object(URLMiddleware, 'get_matched_middleware', mock_match):

            m = URLMiddleware()
            expected_content = "New Response"
            self.assertEquals(m.process_response(request, response).content, expected_content)

    def test_process_exception_no_op(self):

        from urlmiddleware import URLMiddleware

        class MyTemplateResnponseViewMiddleware(object):

            def process_exception(self, request, exception):
                pass

        def mock_match(self, path):
            return [MyTemplateResnponseViewMiddleware(), ]

        request = self.factory.get('/foo/bar/')

        with patch.object(URLMiddleware, 'get_matched_middleware', mock_match):

            m = URLMiddleware()
            e = Exception("Uh oh.")

            self.assertEquals(m.process_exception(request, e), None)

    def test_process_exception(self):

        from urlmiddleware import URLMiddleware

        class MyTemplateResnponseViewMiddleware(object):

            def process_exception(self, request, exception):
                from django.http import HttpResponse
                return HttpResponse("New Response")

        def mock_match(self, path):
            return [MyTemplateResnponseViewMiddleware(), ]

        request = self.factory.get('/foo/bar/')

        with patch.object(URLMiddleware, 'get_matched_middleware', mock_match):

            m = URLMiddleware()
            e = Exception("Uh oh.")

            expected_content = "New Response"
            self.assertEquals(m.process_exception(request, e).content, expected_content)


class MiddlewareRegexURLResolverTestCase(TestCase):

    def test_type_match(self):

        from urlmiddleware.urlresolvers import MiddlewareRegexURLResolver
        from django.core.exceptions import ImproperlyConfigured

        resolver = MiddlewareRegexURLResolver(r'^/', 'test_urlmiddleware.urls_fake')

        with self.assertRaises(ImportError):
            resolver.url_patterns

        resolver = MiddlewareRegexURLResolver(r'^/', 'test_urlmiddleware.urls_empty')

        with self.assertRaises(ImproperlyConfigured):
            resolver.url_patterns


class IncludeMiddleware(TestCase):

    def test_include(self):

        from urlmiddleware.base import MiddlewareResolver404
        from urlmiddleware.urlresolvers import resolve

        with self.assertRaises(MiddlewareResolver404):
            print resolve('/include_test/')

    def test_include_views(self):

        from django.core.exceptions import ImproperlyConfigured
        from urlmiddleware.urlresolvers import resolve

        with self.assertRaises(ImproperlyConfigured):
            print resolve('/include_views_test/')

    def test_include_get(self):

        c = Client()

        response = c.get('/include_test/')

        self.assertEqual(404, response.status_code)
