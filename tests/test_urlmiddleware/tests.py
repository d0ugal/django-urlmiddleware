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
        from test_urlmiddleware.middleware import NoOpMiddleWare, NoOpMiddleWare2

        middleware = resolve('/dotted/')

        self.assertEquals([NoOpMiddleWare, NoOpMiddleWare2, ], middleware)

    def test_duplicated_middleware(self):

        from urlmiddleware.urlresolvers import resolve
        from test_urlmiddleware.middleware import NoOpMiddleWare

        middleware = resolve('/dupe/')

        self.assertEquals([NoOpMiddleWare, ], middleware)

    def test_no_middleware_Action(self):

        c = Client()

        c.get('/')

    def test_middleware(self):

        from urlmiddleware import URLMiddleware

        URLMiddleware()


class MiddlewareTestCase(TestCase):

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

    def test_match_cache(self):

        from urlmiddleware.middleware import _match_cache, URLMiddleware

        self.assertEqual(_match_cache.keys(), [])

        m = URLMiddleware()
        m.get_matched_middleware('/')

        self.assertEqual(_match_cache.keys(), ['/', ])

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
