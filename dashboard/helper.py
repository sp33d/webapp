from django import forms
import logging

from website.models import SiteConfiguration

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
