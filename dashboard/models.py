from django.db import models
from django.utils import timezone
from treebeard.mp_tree import MP_Node


import datetime

class Customer(MP_Node):
    login_name   = models.CharField(max_length=32, unique=True)
    passwd   = models.CharField(max_length=128)
    name     = models.CharField(max_length=32)
    display_pic  = models.ImageField(upload_to='customerdp', blank=True)
    address  = models.CharField(max_length=124, blank=True)
    city     = models.CharField(max_length=32, blank=True)
    mobile_no    = models.CharField(max_length=150, blank=True) 
    email_addr   = models.CharField(max_length=128)
    alert_type   = models.CharField(max_length=15,
                    choices=( ('SMS','SMS'),
                         ('EMAIL','Email'),
                         ('AUTO','Auto'),
                         ('BOTH','Both')
                    ),
                    default='AUTO'      
                  ) 
    role     =  models.CharField(max_length=15,
                    choices=(
                         ('root','Root'), 
                         ('admin','Administrator'),
                         ('dist','Distributor'),
                         ('enduser','End User'),
                         ('endusert1','User Type 1'),
                         ('endusert2','User Type 2')
                    ),
                    default='enduser'
                   )
    dor      = models.DateTimeField(default=timezone.now())
    validity_till = models.DateTimeField(default=timezone.now()+datetime.timedelta(days=30))
    dirty    = models.BooleanField(default=False)

    node_order_by = ['name']

    def __unicode__(self):
        return self.login_name

    def get_serialized_object(self):
        obj = {}
        obj['login_name'] = self.login_name
        obj['passwd'] = 'X' * len(self.passwd)
        obj['name'] = self.name
        if self.display_pic:
            obj['display_pic'] = self.display_pic.url
        else:
            obj['display_pic'] = ''
        obj['address'] = self.address
        obj['city']= self.city
        obj['mobile_no'] = self.mobile_no
        obj['email_addr'] = self.email_addr
        obj['alert_type'] = self.alert_type
        obj['role'] = self.role
        obj['dor'] = int(self.dor.strftime("%s"))
        obj['validity_till'] = int(self.validity_till.strftime("%s"))
        obj['dirty'] = self.dirty
        obj['parent'] = self.get_parent().name
        return obj

class Contact(models.Model):
    owner = models.ForeignKey(Customer)
    contact_value = models.CharField(max_length=128)
    contact_name =  models.CharField(max_length=64)
    contact_type = models.CharField(max_length=32,
                       choices=(
                            ('email','Email'),
                            ('mobileno','Mobile No')
                        ),
                        default='email'
                    )
    dor = models.DateTimeField(default=timezone.now())
    dirty = models.BooleanField(default=False)

    def __unicode__(self):
        return str(self.contact_value)


class FuelTankType(models.Model):
    name    = models.CharField(max_length=32, unique=True)
    level_0     = models.IntegerField()
    level_10    = models.IntegerField()
    level_20    = models.IntegerField()
    level_30    = models.IntegerField()
    level_40    = models.IntegerField()
    level_50    = models.IntegerField()
    level_60    = models.IntegerField()
    level_70    = models.IntegerField()
    level_80    = models.IntegerField()
    level_90    = models.IntegerField()
    level_100   = models.IntegerField()

    def __unicode__(self):
        return self.name

class Device(models.Model):
    imei        = models.CharField(max_length=16, unique=True)
    name        = models.CharField(max_length=32)
    device_type = models.CharField(max_length=32)
    protocol =  models.CharField(max_length=16,
                    choices=( ('TK103','TK103'),
                             ('CT04', 'CT04'),
                             ('PT300','PT300'),
                    ),
                    default= 'TK103'
                )
    icon    = models.CharField(max_length=16,
                    choices=(
                        ('car','Car'),
                        ('bike','Bike'),
                        ('truck','Truck'),
                        ('tracker', 'Tracker'),
                    ),
                    default = 'tracker' 
                )
    imsi       = models.CharField(max_length=16)
    stock_st        = models.CharField(max_length=16,
                                        choices=( ('instock','In Stock'),
                                                 ('sold','Sold'))) 
    tank_sz     = models.IntegerField(default=0) #in Litres
    fuel_tank       = models.ForeignKey(FuelTankType)
    max_speed       = models.IntegerField(default=60) #In KMPH used for alerts
    max_temp        = models.IntegerField(default=50) #In degree Celcius
    lowest_fuel     = models.IntegerField(default=0) #In Litres
    rc_number       = models.CharField(max_length=32, blank=True)
    rc_date     = models.DateField(null=True, blank=True)
    insurance_number    = models.CharField(max_length=32, blank=True)
    insurance_company   = models.CharField(max_length=32, blank=True)
    insurance_date  = models.DateField(null=True, blank=True)
    insurance_due_date  = models.DateField(null=True, blank=True)
    insurance_premium   = models.IntegerField(null=True, blank=True) #in Rupees
    servicing_due_date  = models.DateField(null=True, blank=True)
    servicing_due_km    = models.IntegerField(null=True, blank=True) #In KM
    odometer_reading    = models.IntegerField(null=True, blank=True)
    driver_dp       = models.ImageField(upload_to='driverdp', blank=True)
    driver_name     = models.CharField(max_length=32, blank=True)
    driver_addr     = models.CharField(max_length=256, blank=True)    
    driver_contact_no   = models.CharField(max_length=32, blank=True)
    license_no      = models.CharField(max_length=32, blank=True)
    license_exp_date    = models.DateField(null=True, blank=True)
    contract_company    = models.CharField(max_length=32, blank=True)
    contract_amt    = models.IntegerField(null=True, blank=True)
    contract_renewal_dt = models.DateField(null=True, blank=True)
    contract_date   = models.DateField(null=True, blank=True)
    subscription_amt    = models.IntegerField() #In Rupees
    owner       = models.ForeignKey(Customer)
    dor         = models.DateTimeField(default=timezone.now())
    dirty       = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name 


