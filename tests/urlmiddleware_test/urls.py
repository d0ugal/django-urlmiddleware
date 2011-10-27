from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'urlmiddleware_test.views.home', name='home'),
    # url(r'^urlmiddleware_test/', include('urlmiddleware_test.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

from urlmiddleware_test.middleware import LoginRequiredMiddleware

middlewarepatterns = patterns('',
    url(r'^accounts/', LoginRequiredMiddleware),
    url(r'^accounts/', LoginRequiredMiddleware),
)
