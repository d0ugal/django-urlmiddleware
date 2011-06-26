from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'warewolf_test.views.home', name='home'),
    # url(r'^warewolf_test/', include('warewolf_test.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

from warewolf_test.middleware import LoginRequiredMiddleware

middlewarepatterns = patterns('',
	url(r'^accounts/', LoginRequiredMiddleware),
)