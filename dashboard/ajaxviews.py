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
from django.utils import timezone

import datetime
import json 

from website.models import SiteConfiguration
from dashboard.models import Customer, Contact, FuelTankType, Device
from dashboard.decorators import login_required

import helper
from dashboard.form import CustomerLoginForm, CustomerRegistrationForm, CustomerUpdationForm

logger = logging.getLogger('dashboard.ajaxviews')

@login_required
def customer_tree_json(request):
    result= []
    customer = Customer.objects.get(login_name=request.session["ln"])
    customer_list = customer.get_descendants()
    if customer.is_leaf():
        # If leaf node use different icon
        result.append({ 'id': customer.id,
                        'pId': customer.get_parent().id,
                        'name': customer.name ,
                        'icon': '/static/tree/icons/user-20.png',
                        'itemType': 'lcustomer',
                        })
    else:
        # If Not leaf node use different icon
        result.append({ 'id': customer.id,
                        'pId': 0,
                        'name': customer.name,
                        'iconClose': '/static/tree/icons/user-open-20.png',
                        'iconOpen': '/static/tree/icons/user-close-20.png',
                        'icon': '/static/tree/icons/user-20.png',
                        'itemType': 'customer',
                        })

    # Add the list of devices, which not dirty and sold
    device_list = Device.objects.filter(owner=customer, dirty=False, stock_st='sold')
    for device in device_list:
        result.append({ 'id': device.imei,
                    'pId': customer.id,
                    'name': device.name ,
                    'icon': '/static/tree/icons/device-20.png',
                    'open': True,
                    'itemType': 'ldevice',
                    })  
    for customer in customer_list:
        # Dont list the dirty customer and their devices
        if customer.dirty:
            continue
        if customer.is_leaf():
            # If leaf node use different icon
            result.append({ 'id': customer.id,
                        'pId': customer.get_parent().id,
                        'name': customer.name ,
                        'icon': '/static/tree/icons/user-20.png',
                        'itemType': 'lcustomer',
                        }) 
        else:
            # If Not leaf node use different icon
            result.append({ 'id': customer.id,
                        'pId': customer.get_parent().id,
                        'name': customer.name ,
                        'iconClose': '/static/tree/icons/user-open-20.png',
                        'iconOpen': '/static/tree/icons/user-close-20.png',
                        'icon': '/static/tree/icons/user-20.png',
                        'itemType': 'customer',
                        })
        #Add the list of devices, which are not dirty and sold
        device_list = Device.objects.filter(owner=customer, dirty=False, stock_st='sold')
        for device in device_list:
            result.append({ 'id': device.imei,
                        'pId': customer.id,
                        'name': device.name ,
                        'icon': '/static/tree/icons/device-20.png',
                        'open': True,
                        'itemType': 'ldevice',
                        }) 
    return HttpResponse(json.dumps(result, indent=4), mimetype="application/json")

@login_required
def customer_remove(request):
    result = {}
    result['status'] = 'failed'
    result['error'] = []

    cln = request.POST['ln']
    customer = Customer.objects.get(login_name=request.session["ln"])
    try:
        c = Customer.objects.get(login_name=cln)
    except Customer.DoesNotExist, err:
        result['status'] = 'failed'
        result['error'].append('No such customer.')
        return HttpResponse(json.dumps(result, indent=4), mimetype="application/json")

    if c.dirty:
        result['status'] = 'failed'
        result['error'].append('This customer is already removed.')
        return HttpResponse(json.dumps(result, indent=4), mimetype="application/json")

    if c.login_name == customer.login_name:
        result['status'] = 'failed'
        result['error'].append('Cannot remove logged-in customer.')
        return HttpResponse(json.dumps(result, indent=4), mimetype="application/json")

    if c.is_descendant_of(customer):
        c.dirty = True
        c.save()
        result['status'] = 'success'
        result['msg'] = 'Customer removed successfully.'
        return HttpResponse(json.dumps(result, indent=4), mimetype="application/json")
    else:
        result['status'] = 'failed'
        result['error'].append('Requested customer is not a descendent.')
    return HttpResponse(json.dumps(result, indent=4), mimetype="application/json")


@login_required
def customer_recycle(request):
    result = {}
    result['status'] = 'failed'
    result['error'] = []

    cln = request.POST['ln']
    customer = Customer.objects.get(login_name=request.session["ln"])
    try:
        c = Customer.objects.get(login_name=cln)
    except Customer.DoesNotExist, err:
        result['status'] = 'failed'
        result['error'].append('No such customer.')
        return HttpResponse(json.dumps(result, indent=4), mimetype="application/json")

    if not c.dirty:
        result['status'] = 'failed'
        result['error'].append('This customer is already active.')
        return HttpResponse(json.dumps(result, indent=4), mimetype="application/json")

    if c.is_descendant_of(customer):
        c.dirty = False
        c.save()
        result['status'] = 'success'
        result['msg'] = 'Customer recycled successfully.'
        return HttpResponse(json.dumps(result, indent=4), mimetype="application/json")
    else:
        result['status'] = 'failed'
        result['error'].append('Requested customer is not a descendent.')
    return HttpResponse(json.dumps(result, indent=4), mimetype="application/json")

@login_required
def customer_object(request):
    result = {}
    result['status'] = 'failed'
    result['error'] = []

    cln = request.POST['ln']
    customer = Customer.objects.get(login_name=request.session["ln"])
    try:
        c = Customer.objects.get(login_name=cln)
    except Customer.DoesNotExist, err:
        result['status'] = 'failed'
        result['error'].append('No such customer.')
        return HttpResponse(json.dumps(result, indent=4), mimetype="application/json")

    if c.dirty:
        result['status'] = 'failed'
        result['error'].append('This customer is not active.')
        return HttpResponse(json.dumps(result, indent=4), mimetype="application/json")

    if c.is_descendant_of(customer):
        c.dirty = False
        c.save()
        result['status'] = 'success'
        result['msg'] = 'Customer restored/recycled successfully.'
        result['customer'] = c.get_serialized_object()
        return HttpResponse(json.dumps(result, indent=4), mimetype="application/json")
    else:
        result['status'] = 'failed'
        result['error'].append('Requested customer is not a descendent.')
    return HttpResponse(json.dumps(result, indent=4), mimetype="application/json")


@login_required
def print_customer_updation_form(request):
    result = {}
    result['status'] = 'failed'
    result['error'] = []
    
    cln = request.POST['ln']
    customer = Customer.objects.get(login_name=request.session["ln"])
    try:
        c = Customer.objects.get(login_name=cln)
    except Customer.DoesNotExist, err:
        result['status'] = 'failed'
        result['error'].append('No such customer.')
        return HttpResponse(json.dumps(result, indent=4), mimetype="application/json")

    if c.dirty:
        result['status'] = 'failed'
        result['error'].append('This customer is not active.')
        return HttpResponse(json.dumps(result, indent=4), mimetype="application/json")

    if c.is_descendant_of(customer):
        form = CustomerUpdationForm(request=request)
        result['status'] = 'success'
        result['form'] = form.as_table()    
    else:
        result['status'] = 'failed'
        result['error'].append('Requested customer is not a descendent.')
    return HttpResponse(json.dumps(result, indent=4), mimetype="application/json") 
