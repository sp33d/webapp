from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tracker_in.views.home', name='home'),
    # url(r'^tracker_in/', include('tracker_in.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    # Installing the dashboard app
    url(r'^dashboard/', include('dashboard.urls')),
    # Home page
    url(r'^$', include('website.urls')),
)
