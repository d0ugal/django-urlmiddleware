from django.conf.urls.defaults import patterns, url, include

from urlmiddleware.conf import murl, mpatterns

from test_urlmiddleware.middleware import NoOpMiddleWare, NoOpMiddleWare2

urlpatterns = patterns('django.views.generic.simple',
    url(r'^$', 'direct_to_template', {'template': 'base.html'}),
    url(r'^accounts/$', 'direct_to_template', {'template': 'base.html'}),
    url(r'^no_middleware/$', 'direct_to_template', {'template': 'base.html'}),
)


middlewarepatterns = mpatterns('',
    murl(r'^$', NoOpMiddleWare),
    murl(r'^sub/$', NoOpMiddleWare),
    murl(r'^sub/$', NoOpMiddleWare2),
    murl(r'^dotted/$', 'test_urlmiddleware.middleware.NoOpMiddleWare3'),
    (r'^dotted/$', 'test_urlmiddleware.middleware.NoOpMiddleWare4'),
    murl(r'^dupe/$', 'test_urlmiddleware.middleware.NoOpMiddleWare5'),
    (r'^dupe/$', 'test_urlmiddleware.middleware.NoOpMiddleWare5'),
    murl(r'^include_test/$', include('test_urlmiddleware.urls_include')),
    (r'^include_test/$', include('test_urlmiddleware.urls_include')),
    murl(r'^include_views_test/$', include('test_urlmiddleware.urls_empty')),
)

middlewarepatterns += mpatterns('test_urlmiddleware.middleware',
    murl(r'^dotted2/$', 'NoOpMiddleWare6'),
)
