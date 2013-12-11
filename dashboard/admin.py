from django.contrib import admin
from dashboard.models import Customer, Contact, FuelTankType, Device, Packet

class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        'login_name',
        'name',
        'email_addr',
        'role',
        'dor',
        'validity_till',
        'dirty',
        )

class ContactAdmin(admin.ModelAdmin):
    list_display = (
        'owner',
        'contact_name',
        'contact_value',
        'contact_type',
        'dor',
        'dirty',
        )

class FuelTankTypeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'level_0',
        'level_10',
        'level_20',
        'level_30',
        'level_40',
        'level_50',
        'level_60',
        'level_70',
        'level_80',
        'level_90',
        'level_100',
        )
class DeviceAdmin(admin.ModelAdmin):
    list_display = (
        'imei',
        'imsi',
        'name',
        'protocol',
        'stock_st',
        'tank_sz',
        'fuel_tank',
        'owner',
        'dor',
        'dirty',
        )

class PacketAdmin(admin.ModelAdmin):
    list_display = (
        'device',
        'packet_time',
        'signal',
        'lat',
        'lng',
        'address',
        'speed',
        'orientation',
        'ps',
        'ig',
        'oil',
        'sos',
        'door',
        'mileage',
        'fuel',
        'temprature',
        'dor',
        'dirty',
        )

admin.site.register(Customer, CustomerAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(FuelTankType, FuelTankTypeAdmin)
admin.site.register(Device, DeviceAdmin)
admin.site.register(Packet, PacketAdmin)
