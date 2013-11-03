from django.conf.urls import patterns, include, url


urlpatterns = patterns('',

    #Test page
    url(r'^ref/$', 'dashboard.views.refhome', name='dash_refhome'),
    url(r'^tree/$', 'dashboard.views.tree', name='dash_tree'),
    #Dashboard Home page
    url(r'^$', 'dashboard.views.home', name='dash_home'),
    #Log in/out page
    url(r'^login/$', 'dashboard.views.login', name='dash_login'),
    url(r'^logout/$', 'dashboard.views.logout', name='dash_logout'),
    #Contact Realated Actions
    #Device Related Actions
    url(r'^device-registration/$', 'dashboard.views.device_registration', name='dash_devicereg'),
    url(r'^device-list/$', 'dashboard.views.device_list', name='dash_devicelist'),
    #Customer Related Actions
    url(r'^customer-registration/$', 'dashboard.views.customer_registration', name='dash_custreg'),
    url(r'^customer-list/$', 'dashboard.views.customer_list', name='dash_custlist'),
)


urlpatterns += patterns('',
    #Customer based actions
    url(r'^ajax/customer-tree-json/$', 'dashboard.ajaxviews.customer_tree_json', name='dash_ajax_customer_tree_json'), 
    url(r'^ajax/customer-remove/$', 'dashboard.ajaxviews.customer_remove', name='dash_ajax_customer_remove'), 
    url(r'^ajax/customer-recycle/$', 'dashboard.ajaxviews.customer_recycle', name='dash_ajax_customer_recycle'), 
    url(r'^ajax/customer-object/$', 'dashboard.ajaxviews.customer_object', name='dash_ajax_customer_object'),
    url(r'^ajax/customer-update-form/$', 'dashboard.ajaxviews.print_customer_updation_form', name='dash_ajax_customer_updation_form'),
)
