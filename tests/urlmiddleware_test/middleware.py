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
