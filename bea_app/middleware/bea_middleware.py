from django.core.urlresolvers import reverse,resolve
from django.http import HttpResponseRedirect

class AuthRequiredMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        allowed_pages = ['index','admin','login','logout','register','confirm_email','resend_email']
        response = self.get_response(request)
        if not request.user.is_authenticated() and resolve(request.path_info).url_name not in allowed_pages:
            return HttpResponseRedirect(reverse('index'))

        # Code to be executed for each request/response after
        # the view is called.

        return response
