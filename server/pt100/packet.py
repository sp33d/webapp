import datetime
import time
import json
from django.utils.timezone import utc

class Packet(object):
    imei = None
    signal = None
    lat = None
    lat_ind = None
    lng = None
    lng_ind = None
    speed = None
    orientation = None
    ps = None
    ig = None
    oil = None
    sos = None
    door = None
    high_sensor1 = None
    high_sensor2 = None
    high_sensor3 = None
    low_sensor1 = None
    low_sensor2 = None
    low_sensor3 = None
    fuel = None
    mileage = None
    temp = None
    cellid = None
    packet_type = None
    packet_time = None
    nounce = None #To stop the packet replay
    data = None

    def __unicode__(self):
        return self.imei + ' - ' + packet_time

    """
       @purpose This function is supposed to break the following packed string.
       SA200STTH;861001003125701;111;20131213;06:58:42;47F5;+28.486249;+77.61546;0;299.60;8;1;0000;11.30;0.000;0000000;1;0;0;0074

        Packet Format:
        =============
            I:Data                  Explanation
            ===================================
            0:SA200STTH             Ignore
            1:861001003125701       IMEI
            2:111                   Code
            3:20131213              Date
            4:06:58:42              Time
            5:47F5                  Cellid
            6:+28.486249            Latitiude
            7:+77.61546             Longitude
            8:0                     Speed
            9:299.60                Direction
            10:8                    Satellite
            11:1                    GPS (1-A 0-V)
            12:0000                 Unused
            13:11.30                Fuel
            14:0.000                Temp
            15:0000000              Status (1B - IG, 2B - SOS, 3B - AC, rest unused)
            16:1                    Power status (1/2 - On, 3 - Power Off)
            17:0                    Unused
            18:0                    Unused
            19:0074                 Unused
    """
    def decode_packet(self, pstr, imei="", packet_typ=""):
        pitem = pstr.split(";")
        self.imei = pitem[1]
        self.packet_type = pitem[2]
        try:
            #Make Packet Time
            yy = int(pitem[3][0:4])
            mm = int(pitem[3][4:6])
            dd = int(pitem[3][6:])
            timeitems = pitem[4].split(":")
            hh = int(timeitems[0])
            ii = int(timeitems[1])
            ss = int(timeitems[2])
            self.packet_time = datetime.datetime(yy, mm, dd, hh, ii, ss, tzinfo=utc)
            print "Got ", yy,mm,dd,hh,ii,ss, "Made",self.packet_time, "TS",int(self.packet_time.strftime("%s"))
            #Signal
            if str(pitem[11]) == '1':
                self.signal = 'A'
            else:
                self.signal = 'A'
            #Latitude
            self.lat = float(pitem[6][1:])
            #Latitude Indicator
            self.lat_ind = 'N'
            #Longitude
            self.lng = float(pitem[7][1:])
            #longitude indicator
            self.lng_ind = 'E'
            #Speed
            self.speed = float(pitem[8])
            #Orientation
            self.orientation = pitem[9]
            #Power Status
            if str(pitem[16]) == '1' or str(pitem[16]) == 2:
                self.ps = '1'
            else:
                self.ps = '0'
            #Ignition
            self.ig = pitem[15][0]
            #Breaking the 3rd I/O Byte 
            self.oil = '-1'
            self.sos = pitem[15][1] 
            self.door = pitem[15][2]
            #Breaking the 4th I/O Byte
            self.door = '-1'
            self.high_sensor1 = '-1'
            self.high_sensor2 = '-1'
            self.high_sensor3 = '-1'
            #Breaking the 5th I/O Byte
            self.low_sensor1 = '-1'
            self.low_sensor2 = '-1'
            self.low_sensor3 = '-1'
            #Fuel
            self.fuel = float(pitem[13])
            #Mileage
            self.mileage = '-1'
            #Temprature
            self.temp = pitem[14]
            self.cellid = pitem[5]
            self.nounce = self.imei + '_' + str(time.time())
        except Exception, err:
            print "Error", err
            pass
        self.data = pstr

    def get_serialized_object(self):
        obj = {}
        obj['imei'] = self.imei
        obj['signal'] = self.signal
        obj['lat'] = self.lat
        obj['lat_ind'] = self.lat_ind
        obj['lng'] = self.lng
        obj['lng_ind'] = self.lng_ind
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
        obj['fuel'] = self.fuel
        obj['mileage'] = self.mileage
        obj['packet_type'] = self.packet_type
        obj['packet_time'] = int(self.packet_time.strftime("%s"))
        obj['cellid'] = self.cellid
        obj['temp'] = self.temp
        obj['nounce'] = self.nounce
        obj['data'] = self.data
        return obj

    def get_dict_send(self):
        obj = {}
        obj['password'] = 'u123'
        obj['requestid'] = self.nounce
        obj['id'] = self.imei
        obj['num'] = self.imei
        obj['ver'] = self.packet_type
        obj['mil'] = self.mileage
        obj['lat'] = self.lat
        obj['lon'] = self.lng
        obj['spd'] = self.speed
        obj['dir']= self.orientation
        obj['gpsstatus'] = self.signal
        obj['mps'] = self.ps
        obj['acc'] = self.ig
        obj['oilsupp'] = self.oil
        obj['ps'] = self.ps
        obj['sos'] = self.sos
        obj['alarm']= ''
        obj['cabstatus'] = ''
        obj['vol'] = self.fuel
        obj['aircond'] = self.door
        obj['dt'] = int(self.packet_time.strftime("%s"))
        obj['temp'] = self.temp
        obj['input1'] = ''
        obj['input2'] = ''
        obj['input3'] = ''
        obj['input4'] = ''
        obj['input5'] = ''
        obj['input6'] = ''
        obj['mcc'] = ''
        obj['mnc'] = ''
        obj['lac'] = ''
        obj['cellid'] = self.cellid
        return obj
    
if __name__ == '__main__':
    pck_strs = [
            'SA200STT;861001003138688;111;20131213;17:51:42;EB2A;+28.466271;+77.30237;0;302.05;8;1;0000;11.30;0.000;0000000;1;0;0;6887',
        ]
    
    p = Packet()

    for pck_str in pck_strs:
            p.decode_packet(pck_str)
            print json.dumps(p.get_serialized_object(), indent=4)



class PacketList(object):

    plist = []

    def append(self, item):
        self.plist.append(item)

    def clear(self):
        plist = []

