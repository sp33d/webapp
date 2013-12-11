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
import hashlib
import json

from website.models import SiteConfiguration
from dashboard.models import Customer, Contact, FuelTankType, Device, Packet
from dashboard.decorators import login_required

import helper
from form import CustomerLoginForm, CustomerRegistrationForm, DeviceRegistrationForm

logger = logging.getLogger('dashboard.views')


def refhome(request):
    sc = helper.get_site_conf()
    return render_to_response('dashboardorig.html',{'sconf': sc},context_instance=RequestContext(request))

"""
    Following format of JSON Packets are to be recived from the backend server.
[
    {
        "orientation": "180.99",
        "lng_ind": "E",
        "imei": "088011610051",
        "sos": "0",
        "low_sensor1": "0",
        "lat_ind": "N",
        "high_sensor3": "0",
        "high_sensor2": "0",
        "lng": 77.25513166666666,
        "speed": "000.0",
        "high_sensor1": "0",
        "ig": "0",
        "ps": "0",
        "fuel": 0,
        "mileage": 11125488,
        "low_sensor2": "0",
        "low_sensor3": "0",
        "oil": "0",
        "door": "0",
        "packet_type": "DNRML",
        "lat": 28.578538333333334,
        "data": "131211A2834.7123N07715.3079E000.0043500180.9900000000L00A9C2F0)",
        "signal": "A",
        "packet_time": 1386735120,
        "nounce": "088011610051_1386736505.83"
    },
    {
        "orientation": "183.91",
        "lng_ind": "E",
        "imei": "088011610051",
        "sos": "0",
        "low_sensor1": "0",
        "lat_ind": "N",
        "high_sensor3": "0",
        "high_sensor2": "0",
        "lng": 77.23499166666667,
        "speed": "000.0",
        "high_sensor1": "0",
        "ig": "0",
        "ps": "0",
        "fuel": 0,
        "mileage": 11119447,
        "low_sensor2": "0",
        "low_sensor3": "0",
        "oil": "0",
        "door": "0",
        "packet_type": "DNRML",
        "lat": 28.60056833333333,
        "data": "131210A2836.0341N07714.0995E000.0142637183.9100000000L00A9AB57)",
        "signal": "A",
        "packet_time": 1386684757,
        "nounce": "088011610051_1386736510.45"
    }
]
"""
@csrf_exempt
def api(request):
    result = {}
    try:
        postdata = json.loads(request.body)
    except Exception, err:
        result['status'] = 'error'
        result['error'] = [ str(err) ]
        return HttpResponseBadRequest(json.dumps(result, sort_keys=True, indent=4),mimetype="application/json")
    #Handling Packets
    address_tuples = []
    for packet in postdata:
        address_tuples.append((packet['lat'], packet['lng']))  
    #Parse address
    address = helper.parse_address(address_tuples)   
    for packet in postdata:
        try:
            try:
                device = Device.objects.get(imei=packet['imei'])
            except Device.DoesNotExist, err:
                #No such device is registered, discard its data and move ahead
                logger.error('Got request from unregistered IMEI ', packet['imei'])
                result[packet['nounce']] = 'rejected'
                result[packet['nounce'] + '_str'] = 'No such device is registered.'
                continue
            p = Packet()
            p.device = device
            p.packet_time = datetime.datetime.fromtimestamp(packet['packet_time'])
            p.signal = packet['signal']
            p.lat = packet['lat']
            p.lat_indicator = packet['lat_ind']
            p.lng = packet['lng']
            p.lng_indicator = packet['lng_ind']
            key = str(p.lat) + ':' + str(p.lng)
            if key in address:
                p.address = address[key]
            else:
                p.address = 'Not address available.'
            p.speed = float(packet['speed'])
            p.orientation = float(packet['orientation'])
            p.ps = bool(int(packet['ps']))
            p.ig = bool(int(packet['ig']))
            p.oil = bool(int(packet['oil']))
            p.sos = bool(int(packet['sos']))
            p.door = bool(int(packet['door']))
            p.high_sensor1 = bool(int(packet['high_sensor1']))
            p.high_sensor2 = bool(int(packet['high_sensor2']))
            p.high_sensor3 = bool(int(packet['high_sensor3']))
            p.low_sensor1 = bool(int(packet['low_sensor1']))
            p.low_sensor2 = bool(int(packet['low_sensor2']))
            p.low_sensor3 = bool(int(packet['low_sensor3']))
            p.mileage = packet['mileage']
            p.fuel = packet['fuel']
            p.temprature = 0
            p.save()
            result[packet['nounce']] = 'saved_ok'
        except Exception, err:
            logger.error('Error in storing a packet', err)
            result[packet['nounce']] = 'error'
            result[packet['nounce']+ '_msg'] = str(err)
            pass
    result['status'] = 'ok'
    return HttpResponse(json.dumps(result, sort_keys=True, indent=4),mimetype="application/json")

@login_required
def home(request):
    sc = helper.get_site_conf()
    customer = Customer.objects.get(login_name=request.session["ln"])
    return render_to_response('dashboard.html',
                                {'sconf': sc,
                                 'customer': customer}
                                ,context_instance=RequestContext(request))

def login(request):
    if request.method == 'POST':
        login_form = CustomerLoginForm(data=request.POST)
        if login_form.is_valid():
            login_name = login_form.cleaned_data.get('login_name')
            customer = Customer.objects.get(login_name=login_name)
            request.session["ln"] = customer.login_name
            request.session["name"] = customer.name
            request.session["role"] = customer.role
            request.session["started_at"] = timezone.now().strftime("%s")
            return HttpResponseRedirect('/dashboard/')
        else:
            logger.error('Errors are' + str(login_form.errors))
    else:
        if 'ln' in request.session:
            return HttpResponseRedirect('/dashboard/')
        login_form = CustomerLoginForm()
    sc = helper.get_site_conf()
    return render_to_response('login.html',{'sconf': sc, 'form': login_form },context_instance=RequestContext(request))

def logout(request):
    if 'ln' in request.session:
        request.session.clear()
    return HttpResponseRedirect('/dashboard/login/')

@login_required
def customer_registration(request):
    form_saved = False
    if request.method == 'POST':
        registration_form = CustomerRegistrationForm(data=request.POST, files=request.FILES, request=request)
        if registration_form.is_valid():
            parent = Customer.objects.get(login_name=registration_form.cleaned_data.get('parent'))
            customer = parent.add_child()
            customer.login_name = registration_form.cleaned_data.get('login_name')
            customer.passwd = registration_form.cleaned_data.get('password')
            #Hashing the password
            customer.passwd = hashlib.md5(customer.passwd.encode('utf-8')).hexdigest()
            customer.name  = registration_form.cleaned_data.get('name')
            customer.display_pic = registration_form.cleaned_data.get('display_pic')
            customer.address = registration_form.cleaned_data.get('address')
            customer.city = registration_form.cleaned_data.get('city')
            customer.mobile_no = registration_form.cleaned_data.get('mobile_no')
            customer.email_addr = registration_form.cleaned_data.get('email_addr')
            customer.alert_type = registration_form.cleaned_data.get('alert_type')
            customer.role = registration_form.cleaned_data.get('role')
            validity_till = registration_form.cleaned_data.get('validity_till')
            customer.validity_till = datetime.datetime(validity_till.year, validity_till.month, validity_till.day, 0, 0, 0)
            customer.save()
            form_saved = True
            registration_form = CustomerRegistrationForm(request=request)
        else:
            logger.error('Errors are' + str(registration_form.errors))
    else:
        registration_form = CustomerRegistrationForm(request=request)
    sc = helper.get_site_conf()
    customer = Customer.objects.get(login_name=request.session["ln"])
    return render_to_response('customer-registration.html',{'sconf': sc,
                                                            'customer': customer,
                                                            'form': registration_form,
                                                            'saved': form_saved,
                                                            },context_instance=RequestContext(request))

@login_required
def customer_list(request):
    sc = helper.get_site_conf()
    customer = Customer.objects.get(login_name=request.session["ln"])
    customer_list = customer.get_descendants()
    return render_to_response('customer-list.html',{'sconf': sc,
                                                    'customer': customer,
                                                    'custlist': customer_list
                                                    },context_instance=RequestContext(request))

@login_required
def device_registration(request):
    form_saved = False
    if request.method == 'POST':
        registration_form = DeviceRegistrationForm(data=request.POST, files=request.FILES, request=request)
        if registration_form.is_valid():
            #Save the data
            device = Device()
            device.imei = registration_form.cleaned_data.get('imei')
            device.name = registration_form.cleaned_data.get('name')
            device.device_type = 'normal'
            device.protocol = registration_form.cleaned_data.get('protocol')
            device.icon = registration_form.cleaned_data.get('icon')
            device.imsi = registration_form.cleaned_data.get('imsi')
            device.stock_st = registration_form.cleaned_data.get('stock_st')
            device.tank_sz = registration_form.cleaned_data.get('tank_sz')
            #Get FuelTankType Instance
            fuelTankType = FuelTankType.objects.get(pk=registration_form.cleaned_data.get('fuel_tank'))
            device.fuel_tank = fuelTankType 
            device.max_speed = registration_form.cleaned_data.get('max_speed')
            device.max_temp = registration_form.cleaned_data.get('max_temp')
            device.lowest_fuel = registration_form.cleaned_data.get('lowest_fuel')
            device.rc_number = registration_form.cleaned_data.get('rc_number')
            device.rc_date = registration_form.cleaned_data.get('rc_date')
            device.insurance_number = registration_form.cleaned_data.get('insurance_number')
            device.insurance_company = registration_form.cleaned_data.get('insurance_company')
            device.insurance_date = registration_form.cleaned_data.get('insurance_date')
            device.insurance_due_date = registration_form.cleaned_data.get('insurance_due_date')
            device.insurance_premium = registration_form.cleaned_data.get('insurance_premium')
            device.servicing_due_date = registration_form.cleaned_data.get('servicing_due_date')
            device.servicing_due_km = registration_form.cleaned_data.get('servicing_due_km')
            device.odometer_reading = registration_form.cleaned_data.get('odometer_reading')
            device.driver_dp = registration_form.cleaned_data.get('driver_dp')
            device.driver_name = registration_form.cleaned_data.get('driver_name')
            device.driver_addr = registration_form.cleaned_data.get('driver_addr')
            device.driver_contact_no = registration_form.cleaned_data.get('driver_contact_no')
            device.license_no = registration_form.cleaned_data.get('license_no')
            device.contract_company = registration_form.cleaned_data.get('contract_company')
            device.contract_amt = registration_form.cleaned_data.get('contract_amt')
            device.contract_renewal_dt = registration_form.cleaned_data.get('contract_renewal_dt')
            device.contract_date = registration_form.cleaned_data.get('contract_date')
            device.license_exp_date = registration_form.cleaned_data.get('license_exp_date')
            device.subscription_amt = registration_form.cleaned_data.get('subscription_amt')
            #Get Customer instance
            owner = Customer.objects.get(login_name=registration_form.cleaned_data.get('owner'))
            device.owner = owner
            device.save()
            form_saved = True
            registration_form = DeviceRegistrationForm(request=request)
        else:
            logger.error('Errors are' + str(registration_form.errors))
    else:
        registration_form = DeviceRegistrationForm(request=request) 
    sc = helper.get_site_conf()
    customer = Customer.objects.get(login_name=request.session["ln"])
    customer_list = customer.get_descendants()
    return render_to_response('device-registration.html',{'sconf': sc,
                                                    'customer': customer,
                                                    'form': registration_form,
                                                    'saved': form_saved,
                                                    },context_instance=RequestContext(request))

@login_required
def device_list(request):
    sc = helper.get_site_conf()
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
    return render_to_response('device-list.html',{'sconf': sc,
                                                    'customer': customer,
                                                    'devicelist': device_list
                                                    },context_instance=RequestContext(request))


@login_required
def tree(request):
    sc = helper.get_site_conf()
    customer = Customer.objects.get(login_name=request.session["ln"])
    return render_to_response('tree.html',
                                {'sconf': sc,
                                'customer': customer}
                                ,context_instance=RequestContext(request))


@login_required
def show_map(request):
    sc = helper.get_site_conf()
    customer = Customer.objects.get(login_name=request.session["ln"])
    return render_to_response('map.html',
                                {'sconf': sc,
                                'customer': customer}
                                ,context_instance=RequestContext(request))


@login_required
def summary(request):
    sc = helper.get_site_conf()
    customer = Customer.objects.get(login_name=request.session["ln"])
    return render_to_response('summary.html',
                                {'sconf': sc,
                                'customer': customer}
                                ,context_instance=RequestContext(request))
