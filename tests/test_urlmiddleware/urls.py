from django.conf.urls.defaults import patterns, url

from test_urlmiddleware.middleware import NoOpMiddleWare, NoOpMiddleWare2

urlpatterns = patterns('django.views.generic.simple',
    url(r'^$', 'direct_to_template', {'template': 'base.html'}),
    url(r'^accounts/$', 'direct_to_template', {'template': 'base.html'}),
)


middlewarepatterns = patterns('',
    url(r'^$', NoOpMiddleWare),
    url(r'^sub/$', NoOpMiddleWare),
    url(r'^sub/$', NoOpMiddleWare2),
    url(r'^dotted/$', 'test_urlmiddleware.middleware.NoOpMiddleWare'),
    url(r'^dotted/$', 'test_urlmiddleware.middleware.NoOpMiddleWare2'),
    url(r'^dupe/$', 'test_urlmiddleware.middleware.NoOpMiddleWare'),
    url(r'^dupe/$', 'test_urlmiddleware.middleware.NoOpMiddleWare'),

)
