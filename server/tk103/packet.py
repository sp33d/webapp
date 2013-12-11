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
    packet_type = None
    packet_time = None
    nounce = None #To stop the packet replay
    data = None

    def __unicode__(self):
        return self.imei + ' - ' + packet_time

    """
       @purpose This function is supposed to break the following packed string.
        131210V2836.0440N07714.2401E000.0141343141.3400000000L00A9AB27
    +------+-------------+---------------+-----+---------------------------------------------------------------------+
    | S NO | Feild       | Format        | Sz  |   Explanation                                                       |
    +------+-------------+---------------+-----+---------------------------------------------------------------------+
    | 1.   | Date        | YYMMDD        | 6B  |                                                                     |
    +------+-------------+---------------+-----+---------------------------------------------------------------------+
    | 2.   | Signal      | A/V           | 1B  |  A - GPS Valid, V- GPS is not Valid                                 |
    +------+-------------+---------------+-----+---------------------------------------------------------------------+
    | 3.   | Lat         |               | 9B  |                                                                     |
    +------+-------------+---------------+-----+---------------------------------------------------------------------+
    | 4.   | Lat Ind     | N/S           | 1B  |                                                                     |
    +------+-------------+---------------+-----+---------------------------------------------------------------------+
    | 5.   | Lng         |               | 10B |                                                                     |
    +------+-------------+---------------+-----+---------------------------------------------------------------------+
    | 6.   | Lng Ind     | E/W           | 1B  |                                                                     |
    +------+-------------+---------------+-----+---------------------------------------------------------------------+
    | 7.   | Speed       |               | 5B  |                                                                     |
    +------+-------------+---------------+-----+---------------------------------------------------------------------+
    | 8.   | Time        | HHMMSS        | 6B  | UTC                                                                 |
    +------+-------------+---------------+-----+---------------------------------------------------------------------+
    | 9.   | Orientation |               | 6B  |                                                                     |
    +------+-------------+---------------+-----+---------------------------------------------------------------------+
    | 10.  | I/O State   |               | 8B  | 1st Byte: Main power, 0 is On.                                      |
    |      |             |               |     | 2nd Byte: ACC/Ignition, 1 is On.                                    |
    |      |             |               |     | 3rd Byte: Interpret as Hexadec no (0xF) in binary(0000) bits means: |
    |      |             |               |     |        [ 0 0 0 0 ]                                                  |
    |      |             |               |     |    Oil <-+ | | | (0: Supply, 1: Cut)                                |
    |      |             |               |     |    -X- <---+ | | (Not in use)                                       |
    |      |             |               |     |    SOS <-----+ | (0: Pressed, 1: Open)                              |
    |      |             |               |     |    -X- <-------+ (Not in use)                                       | 
    |      |             |               |     | 4th Byte: Interpret as Hexadec no (0xF) in binary(0000) bits means: |
    |      |             |               |     |        [ 0 0 0 0 ]                                                  |
    |      |             |               |     |    Door<-+ | | | (0: Close, 1: Open)                                |
    |      |             |               |     |    HS1 <---+ | | (0: Not connected/Low, 1: High)                    |
    |      |             |               |     |    HS2 <-----+ | (0: Not connected/Low, 1: High)                    |
    |      |             |               |     |    HS3 <-------+ (0: Not connected/Low, 1: High)                    |
    |      |             |               |     | 5th Byte: Interpret as Hexadec no (0xF) in binary(0000) bits means: |
    |      |             |               |     |        [ 0 0 0 0 ]                                                  |
    |      |             |               |     |    LS1 <-+ | | | (0: Not connected/Low, 1: High)                    |
    |      |             |               |     |    LS2 <---+ | | (0: Not connected/Low, 1: High)                    |
    |      |             |               |     |    LS3 <-----+ | (0: Not connected/Low, 1: High)                    |
    |      |             |               |     |    -X- <-------+ (Not in use)                                       |
    |      |             |               |     | 6th Byte, 7th Byte, 8th Byte: Interpret as Hexadec No (0xFFF) is    | 
    |      |             |               |     |    Fuel.                                                            |
    +------+-------------+---------------+-----+---------------------------------------------------------------------+
    | 11.  | Milepost    | L             | 1B  |                                                                     |
    +------+-------------+---------------+-----+---------------------------------------------------------------------+
    | 12.  | Mileage     |               | 8B  | To be interpreted Hexadecimal String.                               |
    +------+-------------+---------------+-----+---------------------------------------------------------------------+      
    """
    def decode_packet(self, imei, packet_typ, pstr):
        self.imei = imei
        self.packet_type = packet_typ
        try:
            #Make Packet Time
            yy = int('20' + pstr[0:2])
            mm = int(pstr[2:4])
            dd = int(pstr[4:6])
            hh = int(pstr[33:35])
            ii = int(pstr[35:37])
            ss = int(pstr[37:39])
            self.packet_time = datetime.datetime(yy, mm, dd, hh, ii, ss, tzinfo=utc)
            print "Got ", yy,mm,dd,hh,ii,ss, "Made",self.packet_time, "TS",int(self.packet_time.strftime("%s"))
            #Signal
            self.signal = pstr[6]
            #Latitude
            self.lat = float(pstr[7:16]) / 100
            int_part = int(self.lat)
            fixed_fraction_part = (((self.lat - int_part)/60)*100)
            self.lat = int_part + fixed_fraction_part
            #Latitude Indicator
            self.lat_ind = pstr[16]
            #Longitude
            self.lng = float(pstr[17:27]) / 100
            int_part = int(self.lng)
            fixed_fraction_part = (((self.lng - int_part)/60)*100)
            self.lng = int_part + fixed_fraction_part
            #longitude indicator
            self.lng_ind = pstr[27]
            #Speed
            self.speed = pstr[28:33]
            #Orientation
            self.orientation = pstr[39:45]
            #Power Status
            self.ps = pstr[45]
            #Ignition
            self.ig = pstr[46]
            hex_to_bin = {
                    '0': '0000',
                    '1': '0001',
                    '2': '0010',
                    '3': '0011',
                    '4': '0100',
                    '5': '0101',
                    '6': '0110',
                    '7': '0111',
                    '8': '1000',
                    '9': '1001',
                    'A': '1010',
                    'B': '1011',
                    'C': '1100',
                    'D': '1101',
                    'E': '1110',
                    'F': '1111',
                }
            #Breaking the 3rd I/O Byte 
            if pstr[47] in hex_to_bin:
                bits = hex_to_bin[pstr[47]]
            else:
                bits = '0000'
            self.oil = bits[0]
            self.sos = bits[2]
            #Breaking the 4th I/O Byte
            if pstr[47] in hex_to_bin:
                bits = hex_to_bin[pstr[47]]
            else:
                bits = '0000'
            self.door = bits[0]
            self.high_sensor1 = bits[1]
            self.high_sensor2 = bits[2]
            self.high_sensor3 = bits[3]
            #Breaking the 5th I/O Byte
            if pstr[48] in hex_to_bin:
                bits = hex_to_bin[pstr[48]]
            else:
                bits = '0000'
            self.low_sensor1 = bits[0]
            self.low_sensor2 = bits[1]
            self.low_sensor3 = bits[2]
            #Fuel
            self.fuel = int(pstr[50:53], 16)
            #Mileage
            self.mileage = int(pstr[54:62], 16)
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
        obj['nounce'] = self.nounce
        obj['data'] = self.data
        return obj


if __name__ == '__main__':
    pck_strs = [
            '(088011610051BR00131210V2836.0440N07714.2401E000.0141343141.3400000000L00A9AB27)',
            '(088011610051BP05000088011610051131210A2836.0440N07714.2401E000.0141323141.3400000000L00A9AB27)',
            '(088011610051BP05000088011610051131210A2836.0440N07714.2401E000.0141323141.3400000000L00A9AB27)'
        ]
    
    p = Packet()

    for pck_str in pck_strs:
        if  pck_str[13:17] == 'BR00':
            imei = pck_str[1:13]
            p.decode_packet(imei, 'DNRML', pck_str[17:])
            print json.dumps(p.get_serialized_object(), indent=4)
        elif pck_str[13:17] == 'BP05':
            imei = pck_str[1:13]
            p.decode_packet(imei, 'LOGIN', pck_str[32:])
            print json.dumps(p.get_serialized_object(), indent=4)
        else:
            print "Skipping", pck_str



class PacketList(object):

    plist = []

    def append(self, item):
        self.plist.append(item)

    def clear(self):
        plist = []

