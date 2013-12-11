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
import hashlib

from website.models import SiteConfiguration
from dashboard.models import Customer, Contact, FuelTankType, Device, Packet
from dashboard.decorators import login_required

import helper
from dashboard.form import CustomerLoginForm, CustomerRegistrationForm, CustomerUpdationForm, \
    DeviceUpdationForm

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
        result['status'] = 'success'
        result['msg'] = 'Customer object serialized successfully.'
        result['customer'] = c.get_serialized_object()
        return HttpResponse(json.dumps(result, indent=4), mimetype="application/json")
    else:
        result['status'] = 'failed'
        result['error'].append('Requested customer is not a descendent.')
    return HttpResponse(json.dumps(result, indent=4), mimetype="application/json")


@login_required
def customer_update(request):
    result = {}
    result['status'] = 'failed'
    result['error'] = []
    form_saved = False
    if 'ln' in request.POST:
        cln = request.POST['ln']
    else:
        cln = request.POST['login_name']
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
        if request.method == 'POST' and request.is_ajax() and 'name' in request.POST:
            form = CustomerUpdationForm(data=request.POST, files=request.FILES, request=request)
            if form.is_valid():
                ln = form.cleaned_data.get('login_name')
                cust = Customer.objects.get(login_name=ln)
                temp = form.cleaned_data.get('password')
                if not temp == "":
                    cust.passwd = hashlib.md5(temp.encode('utf-8')).hexdigest()
                cust.name = form.cleaned_data.get('name')
                temp = form.cleaned_data.get('display_pic')
                if temp:
                    cust.display_pic = temp
                cust.address = form.cleaned_data.get('address')
                cust.city = form.cleaned_data.get('city')
                cust.mobile_no = form.cleaned_data.get('mobile_no')
                cust.email_addr = form.cleaned_data.get('email_addr')
                cust.alert_type = form.cleaned_data.get('alert_type')
                cust.role = form.cleaned_data.get('role')
                validity_till = form.cleaned_data.get('validity_till')
                cust.validity_till = datetime.datetime(validity_till.year, validity_till.month, validity_till.day, 0, 0, 0)
                cust.save()
                form_saved = True              
                form = CustomerUpdationForm(request=request) 
            else:
                logger.error('Errors are' + str(form.errors)) 
        else: 
            form = CustomerUpdationForm(request=request)
        result['status'] = 'success'
        result['form'] = form.as_table()   
        result['form_saved'] = form_saved 
    else:
        result['status'] = 'failed'
        result['error'].append('Requested customer is not a descendent.')
    return HttpResponse(json.dumps(result, indent=4), mimetype="application/json")


@login_required
def device_remove(request):
    result = {}
    result['status'] = 'failed'
    result['error'] = []

    did = request.POST['did']
    customer = Customer.objects.get(login_name=request.session["ln"])
    try:
        d = Device.objects.get(imei=did)
        c = d.owner
    except Customer.DoesNotExist, err:
        result['status'] = 'failed'
        result['error'].append('No such device.')
        return HttpResponse(json.dumps(result, indent=4), mimetype="application/json")

    if d.dirty:
        result['status'] = 'failed'
        result['error'].append('This device is already removed.')
        return HttpResponse(json.dumps(result, indent=4), mimetype="application/json")

    if c.is_descendant_of(customer) or c.id == customer.id:
        d.dirty = True
        d.save()
        result['status'] = 'success'
        result['msg'] = 'Device removed successfully.'
        return HttpResponse(json.dumps(result, indent=4), mimetype="application/json")
    else:
        result['status'] = 'failed'
        result['error'].append('Requested device is not a descendent.')
    return HttpResponse(json.dumps(result, indent=4), mimetype="application/json")

@login_required
def device_recycle(request):
    result = {}
    result['status'] = 'failed'
    result['error'] = []

    did = request.POST['did']
    customer = Customer.objects.get(login_name=request.session["ln"])
    try:
        d = Device.objects.get(imei=did)
        c = d.owner
    except Customer.DoesNotExist, err:
        result['status'] = 'failed'
        result['error'].append('No such device.')
        return HttpResponse(json.dumps(result, indent=4), mimetype="application/json")

    if not d.dirty:
        result['status'] = 'failed'
        result['error'].append('This device is already active.')
        return HttpResponse(json.dumps(result, indent=4), mimetype="application/json")

    if c.is_descendant_of(customer) or c.id == customer.id:
        d.dirty = False
        d.save()
        result['status'] = 'success'
        result['msg'] = 'Device recycled successfully.'
        return HttpResponse(json.dumps(result, indent=4), mimetype="application/json")
    else:
        result['status'] = 'failed'
        result['error'].append('Requested device is not a descendent.')
    return HttpResponse(json.dumps(result, indent=4), mimetype="application/json")

@login_required
def device_object(request):
    result = {}
    result['status'] = 'failed'
    result['error'] = []

    did = request.POST['did']
    customer = Customer.objects.get(login_name=request.session["ln"])
    try:
        d = Device.objects.get(imei=did)
        c = d.owner
    except Customer.DoesNotExist, err:
        result['status'] = 'failed'
        result['error'].append('No such device.')
        return HttpResponse(json.dumps(result, indent=4), mimetype="application/json")

    if d.dirty:
        result['status'] = 'failed'
        result['error'].append('This device is not active.')
        return HttpResponse(json.dumps(result, indent=4), mimetype="application/json")

    if c.is_descendant_of(customer) or c.id == customer.id:
        result['status'] = 'success'
        result['msg'] = 'Device serialized successfully.'
        result['device'] = d.get_serialized_object()
        return HttpResponse(json.dumps(result, indent=4), mimetype="application/json")
    else:
        result['status'] = 'failed'
        result['error'].append('Requested device is not a descendent.')
    return HttpResponse(json.dumps(result, indent=4), mimetype="application/json")


@login_required
def device_update(request):
    result = {}
    result['status'] = 'failed'
    result['error'] = []
    form_saved = False
    if 'did' in request.POST:
        did = request.POST['did']
    else:
        did = request.POST['imei']
    customer = Customer.objects.get(login_name=request.session["ln"])

    try:
        d = Device.objects.get(imei=did)
        c = d.owner
    except Device.DoesNotExist, err:
        result['status'] = 'failed'
        result['error'].append('No such device.')
        return HttpResponse(json.dumps(result, indent=4), mimetype="application/json")

    if d.dirty:
        result['status'] = 'failed'
        result['error'].append('This device is not active.')
        return HttpResponse(json.dumps(result, indent=4), mimetype="application/json")

    if c.is_descendant_of(customer) or c.id == customer.id:
        if request.method == 'POST' and request.is_ajax() and 'imei' in request.POST:
            form = DeviceUpdationForm(data=request.POST, files=request.FILES, request=request)
            if form.is_valid():
                #device.imei = form.cleaned_data.get('imei')
                device = d
                device.name = form.cleaned_data.get('name')
                device.device_type = 'normal'
                device.protocol = form.cleaned_data.get('protocol')
                device.icon = form.cleaned_data.get('icon')
                device.imsi = form.cleaned_data.get('imsi')
                device.stock_st = form.cleaned_data.get('stock_st')
                device.tank_sz = form.cleaned_data.get('tank_sz')
                #Get FuelTankType Instance
                fuelTankType = FuelTankType.objects.get(pk=form.cleaned_data.get('fuel_tank'))
                device.fuel_tank = fuelTankType
                device.max_speed = form.cleaned_data.get('max_speed')
                device.max_temp = form.cleaned_data.get('max_temp')
                device.lowest_fuel = form.cleaned_data.get('lowest_fuel')
                device.rc_number = form.cleaned_data.get('rc_number')
                device.rc_date = form.cleaned_data.get('rc_date')
                device.insurance_number = form.cleaned_data.get('insurance_number')
                device.insurance_company = form.cleaned_data.get('insurance_company')
                device.insurance_date = form.cleaned_data.get('insurance_date')
                device.insurance_due_date = form.cleaned_data.get('insurance_due_date')
                device.insurance_premium = form.cleaned_data.get('insurance_premium')
                device.servicing_due_date = form.cleaned_data.get('servicing_due_date')
                device.servicing_due_km = form.cleaned_data.get('servicing_due_km')
                device.odometer_reading = form.cleaned_data.get('odometer_reading')
                if form.cleaned_data.get('driver_dp'):
                    device.driver_dp = form.cleaned_data.get('driver_dp')
                device.driver_name = form.cleaned_data.get('driver_name')
                device.driver_addr = form.cleaned_data.get('driver_addr')
                device.driver_contact_no = form.cleaned_data.get('driver_contact_no')
                device.license_no = form.cleaned_data.get('license_no')
                device.contract_company = form.cleaned_data.get('contract_company')
                device.contract_amt = form.cleaned_data.get('contract_amt')
                device.contract_renewal_dt = form.cleaned_data.get('contract_renewal_dt')
                device.contract_date = form.cleaned_data.get('contract_date')
                device.license_exp_date = form.cleaned_data.get('license_exp_date')
                device.subscription_amt = form.cleaned_data.get('subscription_amt')
                owner = Customer.objects.get(login_name=form.cleaned_data.get('owner'))
                device.owner = owner
                device.save()
                form_saved = True
                form = DeviceUpdationForm(request=request)
            else:
                logger.error('Errors are' + str(form.errors))
        else:
            form = DeviceUpdationForm(request=request)
        result['status'] = 'success'
        result['form'] = form.as_table()
        result['form_saved'] = form_saved
    else:
        result['status'] = 'failed'
        result['error'].append('Requested device is not a descendent.')
    return HttpResponse(json.dumps(result, indent=4), mimetype="application/json")

@login_required
def summary(request):
    result = {}
    result['status'] = 'failed'
    result['error'] = []

    customer = Customer.objects.get(login_name=request.session["ln"])
    customer_list = customer.get_descendants()
    device_list = []
    devices = customer.device_set.all()
    if len(devices) > 0:
        device_list += devices
    for cust in customer_list:
        devices = cust.device_set.all()
        if len(devices) > 0:
            device_list += devices

    result['summary'] = []
    for device in device_list:
        summary_record = {}
        try:
            packet = device.packet_set.latest('packet_time')
        except Packet.DoesNotExist, err:
            packet = None
            pass
        summary_record['imei'] = device.imei
        summary_record['name'] = device.name
        if packet is None:
            summary_record['time'] = 0
            summary_record['packet'] = packet
        else:
            summary_record['packet'] = packet.get_serialized_object()
            summary_record['time'] = int(packet.packet_time.strftime("%s"))
        result['summary'].append(summary_record)

    result['summary']  = sorted(result['summary'], key=lambda k: k['time'])
    result['summary'].reverse()
    result['status'] = 'ok'
    return HttpResponse(json.dumps(result, indent=4), mimetype="application/json") 
