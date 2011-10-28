from django.test import TestCase
from django.test.client import Client


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

    def test_no_middleware_Action(self):

        c = Client()

        c.get('/')


    def test_middleware(self):

        from urlmiddleware import URLMiddleware