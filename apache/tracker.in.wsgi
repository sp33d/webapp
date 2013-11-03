import os
import sys
sys.path = ['/var/www/'] + ['/var/www/tracker_in'] + ['/var/www/tracker_in/tracker_in'] + sys.path
os.environ['DJANGO_SETTINGS_MODULE'] = 'tracker_in.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
