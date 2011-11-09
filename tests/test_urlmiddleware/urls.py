from django.conf.urls.defaults import patterns, url, include
from django.views.generic import TemplateView

from urlmiddleware.conf import middleware, mpatterns

from test_urlmiddleware.middleware import NoOpMiddleWare, NoOpMiddleWare2


urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='base.html')),
    url(r'^accounts/$', TemplateView.as_view(template_name='base.html')),
    url(r'^no_middleware/$', TemplateView.as_view(template_name='base.html')),
)


middlewarepatterns = mpatterns('',
    middleware(r'^$', NoOpMiddleWare),
    middleware(r'^sub/$', NoOpMiddleWare),
    middleware(r'^sub/$', NoOpMiddleWare2),
    middleware(r'^dotted/$', 'test_urlmiddleware.middleware.NoOpMiddleWare3'),
    (r'^dotted/$', 'test_urlmiddleware.middleware.NoOpMiddleWare4'),
    middleware(r'^dupe/$', 'test_urlmiddleware.middleware.NoOpMiddleWare5'),
    (r'^dupe/$', 'test_urlmiddleware.middleware.NoOpMiddleWare5'),
    middleware(r'^include_test/', include('test_urlmiddleware.urls_include')),
    (r'^include_test/', include('test_urlmiddleware.urls_include')),
    middleware(r'^include_views_test/', include('test_urlmiddleware.urls_empty')),
)

middlewarepatterns += mpatterns('test_urlmiddleware.middleware',
    middleware(r'^dotted2/$', 'NoOpMiddleWare6'),
)
