from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.http import HttpResponse, HttpResponseServerError
from django.http import HttpResponseBadRequest
import traceback, pprint
from django.template import RequestContext
from django import forms
from django.views.decorators.csrf import csrf_exempt
import logging, json, pprint
from django.views.decorators.csrf import ensure_csrf_cookie
from django.template import Context, loader
from django.utils.safestring import mark_safe
from django.http import Http404

from website.models import SiteConfiguration 

logger = logging.getLogger('website.views')

def home(request):
    sc = False
    try:
        scs = SiteConfiguration.objects.all()
        if len(scs):
            sc = scs[0]
        else:
            sc = SiteConfiguration.set_and_get_default()
    except Exception, err:
        logger.error(err)
    return render_to_response('index.html',{'sconf': sc},context_instance=RequestContext(request))
