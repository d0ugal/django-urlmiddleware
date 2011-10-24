Django urlmiddleware
========================================

This app allows you to define middleware in your Django project based on url
configurations rather than adding middleware globally to every single request.


Why?
========================================

Adding middleware globally is not always a good thing. You may only want it
to take effect on certain areas in your website. Third party apps can also
then include their middleware definitions in the url.py file and remove the
need for you to modify global settings.


Quick Start
========================================

Install urlmiddleware::

    pip install urlmiddleware

There is no need to add it to your installed apps, however, you do need to
register one global middleware class that will then control the url based
middleware::

    MIDDLEWARE_CLASSES = (
        # ...
        # add urlmiddleware after all other middleware.
        'urlmiddleware.middleware.UrlMiddlewareMiddleware',
    )

Start adding middleware to your project in your url.py files below your normal
url definitions::

    middlewarepatterns = patterns('',
        url(r'^myapp/', MyMiddleWareClass),
    )

A common example is using this technique to add login required to whole sub
sections of your url tree. First you need to create a LoginRequiredMiddleware::

    from django.conf import settings
    from django.contrib.auth.views import login
    from django.http import HttpResponseRedirect

    class LoginRequiredMiddleware(object):

        def process_request(self, request):

            login_path = settings.LOGIN_URL

            if request.path != login_path and request.user.is_anonymous():
                if request.POST:
                    return login(request)
                else:
                    return HttpResponseRedirect('%s?next=%s' % (login_path, request.path))

Then in your urls.py file::

    from myapp.middleware import LoginRequiredMiddleware

    middlewarepatterns = patterns('',
        url(r'^accounts/', LoginRequiredMiddleware),
    )

Done!