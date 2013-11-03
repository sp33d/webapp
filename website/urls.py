from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    # Home page
    url(r'^$', 'website.views.home', name='website_home'),
)
