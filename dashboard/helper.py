from django import forms
import logging
import settings 
import requests, json

from website.models import SiteConfiguration
from dashboard.models import Address

logger = logging.getLogger('helper')

def get_site_conf():
    sc = False
    try:
        scs = SiteConfiguration.objects.all()
        if len(scs):
            sc = scs[0]
        else:
            sc = SiteConfiguration.set_and_get_default()
    except Exception, err:
        logger.error(err)
    return sc



def get_inferior_roles(role):
    inferior_roles = {
                'root': ( 
                    ('admin','Administrator'),
                    ('dist','Distributor'),
                    ('enduser','End User'),
                    ('endusert1','User Type 1'),
                    ('endusert2','User Type 2') ,   
                ),
                'admin': (
                    ('dist','Distributor'),
                    ('enduser','End User'),
                    ('endusert1','User Type 1'),
                    ('endusert2','User Type 2') ,
                ),
                'dist': (
                    ('enduser','End User'),
                    ('endusert1','User Type 1'),
                    ('endusert2','User Type 2') ,
                ), 
                'enduser': (
                    ('','None'),
                ),
                'endusert1': (
                    ('','None'),
                ),
                'endusert2': (
                    ('','None'),
                ),
                'DEFAULT':  (
                    ('','None'),
                ),
            }

    if role in inferior_roles:
        return inferior_roles[role]
    return inferior_roles['DEFAULT'] 

def parse_address_remotely(lat_lng_tuples):
    result = {}
    data_to_post = []
    for lat, lng in lat_lng_tuples:
        record = {}
        record['lat'] = lat
        record['lng'] = lng
        data_to_post.append(record)
        
    url = settings.RGEOCODING_URL
    headers = {'content-type': 'application/json'}
    r = requests.post(url, data=json.dumps(data_to_post), headers=headers)
    if r.status_code == 200:
        response = r.text
        result =  json.loads(response)
        return result
    return False


def parse_address(lat_lng_tuples):
    result = []
    parse_remotely = []
    for lat, lng in lat_lng_tuples:
        #Check Locally
        add = Address.get_address(lat, lng)
        if add is not None:
            print "Parsed locally:", lat, lng
            result[str(lat) + ':' + str(lng)] = add
        else:
            print "Parsed remotely:", lat, lng
            parse_remotely.append((lat,lng))
    #If there are items for remote parsing, do it
    response = parse_address_remotely(parse_remotely)
    if response:
        for key in response.keys():
            result[key] = response[key]
    return result
