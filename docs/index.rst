Django urlmiddleware
========================================

This app allows you to define middleware in your Django project based on url
configurations rather than adding middleware globally to every single request.


Why?
========================================

Adding middleware globally is not always a good thing. You may only want it
to take effect on certain areas in your website. Third party apps can also
then include their middleware definitions in the url.py file and remove the
need for you to modify global settings. This also removed the overhead of
running middleware against urls where it will never be needed. It's a fairly
common pattern to re-invent url mapping in middleware by checking the path to
see if the middleware should be applied or not, this is no longer needed if you
use urlmiddleware.


Quick Start
========================================

Install urlmiddleware::

    pip install urlmiddleware

There is no need to add urlmiddlewware to your installed apps, however, you do
need to register one global middleware class that will act as the entry point
for url based middleware::

    MIDDLEWARE_CLASSES = (
        # ...
        # add urlmiddleware after all other middleware.
        'urlmiddleware.URLMiddleware',
    )

Once you have registered the middleware class, you can start adding middleware
to your project in your urls.py files alongside your normal url definitions::

    middlewarepatterns = patterns('',
        url(r'^myapp/', MyMiddleWareClass),
    )

A common example usecase is adding a login required restriction on a while site
or a while subsection, for example requireing the user to be logged in for
everything under /accounts/. First you need to create a
LoginRequiredMiddleware::

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

Then you can add it to your urls.py file just like you would with a view.

    from myapp.middleware import LoginRequiredMiddleware

    middlewarepatterns = patterns('',
        url(r'^accounts/', LoginRequiredMiddleware),
    )

That example shows the middleware being imported into urls.py but its worth
noting thatyou can also add it in the same way you would add views. For example
`url(r'^accounts/', 'myapp.middleware.LoginRequiredMiddleware')`

And then you should be done.

Requirements
============
The only requirement for urlmiddleware is Django >= 1.3. It may be possible to
use it with lesser versions of Django but testing and development is carried out
of 1.3 and above.

Contents
========

.. toctree::
 :maxdepth: 1

 changelog