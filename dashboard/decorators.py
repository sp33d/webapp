from dashboard.models import Customer
from django.http import HttpResponseRedirect, HttpResponse
from django.core.exceptions import PermissionDenied

def login_required(orig_func):
    def wrap(request, *args, **kwargs):
        if ("ln" not in request.session):
            if request.is_ajax():
                return HttpResponse("unauthenticated", mimetype="text/plain")
            request.session.clear()
            return HttpResponseRedirect('/dashboard/login')
                
        authenticated = True

        if authenticated:
            return orig_func(request, *args, **kwargs)
        else:
            if request.is_ajax():
                return HttpResponse("unauthenticated", mimetype="text/plain")
            request.session.clear()
            return HttpResponseRedirect('/dashboard/login')

    wrap.__doc__ = orig_func.__doc__
    wrap.__name__ = orig_func.__name__
    return wrap

