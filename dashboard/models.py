from django.db import models
from django.utils import timezone
from treebeard.mp_tree import MP_Node
import redis
import logging
import datetime
from django.conf import settings

redisClient = redis.Redis(host='localhost', port=6379, db=0)
logger = logging.getLogger('dashboard.models')

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
                         ('root','Root'), #pick this from table
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
        obj['object'] = 'Customer'
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
                    choices=( ('TK103','TK103'),  #pick this from config file
                             ('CT04', 'CT04'),
                             ('PT300','PT300'),
                    ),
                    default= 'TK103'
                )
    icon    = models.CharField(max_length=16,
                    choices=(
                        ('car','Car'),  # we give each icon a number and then place in folder n later select icon from that number and save a number in table say 1...255
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

    def get_serialized_object(self):
        obj = {}
        obj['object'] = 'Device'
        obj['imei'] = self.imei
        obj['name'] = self.name
        obj['device_type'] = self.device_type
        obj['protocol'] = self.protocol
        obj['icon'] = self.icon
        obj['imsi'] = self.imsi
        obj['stock_st'] = self.stock_st
        obj['tank_sz'] = self.tank_sz
        obj['fuel_tank'] = self.fuel_tank.name
        obj['max_speed'] = self.max_speed
        obj['max_temp'] = self.max_temp
        obj['lowest_fuel'] = self.lowest_fuel
        obj['rc_number'] = self.rc_number
        obj['rc_date'] = self.rc_date
        obj['insurance_number'] = self.insurance_number
        obj['insurance_company'] = self.insurance_company
        obj['insurance_date'] = self.insurance_date
        obj['insurance_due_date'] = self.insurance_due_date
        obj['insurance_premium'] = self.insurance_premium
        obj['servicing_due_date'] = self.servicing_due_date
        obj['servicing_due_km'] = self.servicing_due_km
        obj['odometer_reading'] = self.odometer_reading
        if  self.driver_dp:
            obj['driver_dp'] = self.driver_dp.url
        else:
            obj['driver_dp'] = ''
        obj['driver_name'] = self.driver_name
        obj['driver_addr'] = self.driver_addr
        obj['driver_contact_no'] = self.driver_contact_no
        obj['license_no'] = self.license_no
        obj['license_exp_date'] = self.license_exp_date
        obj['contract_company'] = self.contract_company
        obj['contract_amt'] = self.contract_amt
        obj['contract_renewal_dt'] = self.contract_renewal_dt
        obj['contract_date'] = self.contract_date
        obj['subscription_amt'] = self.subscription_amt
        obj['owner'] = self.owner.name
        obj['dor'] = int(self.dor.strftime("%s"))
        obj['dirty'] = self.dirty
        return obj 

class Packet(models.Model):
    device = models.ForeignKey(Device)
    packet_time = models.DateTimeField(default=timezone.now())
    # Location Details
    signal = models.CharField(max_length=2, default='A')
    lat = models.FloatField(default=None, null=True)
    lat_indicator = models.CharField(max_length=1, default='')
    lng = models.FloatField(default=None, null=True)
    lng_indicator = models.CharField(max_length=1, default='')
    address = models.CharField(max_length=64, default='NA')
    speed = models.FloatField(default=None, null=True)
    orientation = models.FloatField(default=None, null=True)
    # I/O States
    ps =  models.BooleanField(default=False)
    ig =  models.BooleanField(default=False)
    oil =  models.BooleanField(default=False)
    sos =  models.BooleanField(default=False)
    door =  models.BooleanField(default=False)
    high_sensor1 =  models.BooleanField(default=False)
    high_sensor2 =  models.BooleanField(default=False)
    high_sensor3 =  models.BooleanField(default=False)
    low_sensor1 =  models.BooleanField(default=False)
    low_sensor2 =  models.BooleanField(default=False)
    low_sensor3 =  models.BooleanField(default=False)
    mileage =  models.FloatField(default=None, null=True)
    # Analog I/O Values
    fuel = models.FloatField(default=None, null=True)
    temprature = models.FloatField(default=None, null=True)
    #House Keeping Items
    dor         = models.DateTimeField(default=timezone.now())
    dirty       = models.BooleanField(default=False)

    def __unicode__(self):
        return str(self.device.imei) + str(self.packet_time.strftime("%s"))

    def get_serialized_object(self):
        obj = {}
        obj['object'] = 'Packet'
        obj['imei'] = self.device.imei
        obj['name'] = self.device.name
        obj['device_type'] = self.device.device_type
        obj['packet_time'] = int(self.packet_time.strftime("%s"))
        obj['signal'] = self.signal
        obj['lat'] = self.lat
        obj['lat_indicator'] = self.lat_indicator
        obj['lng'] = self.lng
        obj['lng_indicator'] = self.lng_indicator
        obj['address'] = self.address
        obj['speed'] = self.speed
        obj['orientation'] = self.orientation
        obj['ps'] = self.ps
        obj['ig'] = self.ig
        obj['oil'] = self.oil
        obj['sos'] = self.sos
        obj['door'] = self.door
        obj['high_sensor1'] = self.high_sensor1
        obj['high_sensor2'] = self.high_sensor2
        obj['high_sensor3'] = self.high_sensor3
        obj['low_sensor1'] = self.low_sensor1
        obj['low_sensor2'] = self.low_sensor2
        obj['low_sensor3'] = self.low_sensor3
        obj['mileage'] = self.mileage
        obj['fuel'] = self.fuel
        obj['temprature'] = self.temprature
        obj['dor']= int(self.dor.strftime("%s"))
        obj['dirty'] = self.dirty
        return obj


class Address(object):
    """
        Redis Object: Used to create a local Address database repository for fequently used data
            this will help in reducing the Network call and waiting to remote reverse geocoding server.

        add -- hashtable
             lat:lng     -- key which stores the address at lat(xx.xxx) and lng(xx.xxx) 
    """

    lat = None
    lng = None
    address = None

    @staticmethod
    def get_address(plat, plng):
        plat = str(plat)[0:6]
        plng = str(plng)[0:6]
        add = redisClient.hget("add", plat+":"+plng)
        return add  #Note: if the address is not in local Redis DB, None will be returned

    @staticmethod
    def set_address(plat, plng, address):
        plat = str(plat)[0:6]
        plng = str(plng)[0:6]
        key = plat+":"+plng
        if len(key) and len(address):
            redisClient.hset("add", key, address)
            return True
        return False

