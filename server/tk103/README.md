#A TK103 Server
based on docs from http://location.io/files/2013/04/GPS-Tracker-Communication-Protocol.pdf
#Description
This is a very basic implementation of the TK103 pprotocol, to collect the GPS data and alarms in a optimal way.
altough much more optimization is pending.

this code is based on the https://github.com/durian/tk102-server
#Squence diagram of Client-Server Dialogue
1. TK103 TCP server starts listening on a specified HOST and PORT.
2. TK103 client  connects to the server and sends the Enrollment/Login/Registration Packet.
    the communication can be graphically shown as:
    
    ```
    +-------------+                                                     +-------------+
    |   Server    |                                                     |   Client    |
    +-------------+                                                     +-------------+
    |                                                                                /|<----------------+
    |                                                                               / |                 |
    |<------------------------------Login/Enrollment Packet------------------------/  |                 |
    |\                                                                                |                 |
    | \-----------------------------Response to Login Packet------------------------->|                 |
    |                                                                                 |                 |
    |                                                                                /|<------------+   |
    |                                                                               / |             |   |
    |<-------------------------------Feedback/Alaram Packet------------------------/  |             |   |
    |\                                                                                |             |   |
    | \------------------------------Respond to Alarm Packet------------------------->|             |   |
    |                                                                                 |             |   |
    |                                                                                /|             |   |
    |                                                                               / |             |   |
    |<---------------------------------Handshake Packet----------------------------/  |             |   |
    |\                                                                                |             |   |
    | \-------------------------------Response to Handshake-------------------------->| if ok: -----+   |
    |                                                                                 | else:  ---------+   
    |                                                                                 |
    ```

3. Terminate the server.

#Login/Enrollment Request Packet (Device to Server)
    
    +------+-----------+------+-----------------+---------------------+------+
    | Head | Device ID | CMD  | 000 + Device ID | GPS Data            | Tail |
    +------+-----------+------+-----------------+---------------------+------+

    |<-1B->|<- 12B   ->|<-4B->|<-15B          ->|<-60B              ->|<-1B->|

e.g. <code>(013612345678BP05000013612345678080524A2232.9806N11304.9355E000.1101241323.8700000000L000450AC)</code>

1. <code>(</code>: Head
2. <code>013612345678</code>: Device ID
3. <code>BP05</code>: Command
4. <code>000013612345678</code>: 000 + Device ID
5. <code>080524A2232.9806N11304.9355E000.1101241323.8700000000L000450AC</code>: GPS Data
6. <code>)</code>: Tail

#Login/Enrollment Response Packet (Server to Device)
    
    +------+-----------+------+------+
    | Head | Device ID | CMD  | Tail |
    +------+-----------+------+------+

    |<-1B->|<- 12B   ->|<-4B->|<-1B->|

e.g. <code>(013612345678AP05)</code>

1. <code>(</code>: Head
2. <code>013612345678</code>: Device ID
3. <code>AP05</code>: Command
4. <code>)</code>: Tail
 
#Feedback Data Packet (Device to Server)

    +------+-----------+------+---------------------+------+
    | Head | Device ID | CMD  | GPS Data            | Tail |
    +------+-----------+------+---------------------+------+

    |<-1B->|<- 12B   ->|<-4B->|<-60B              ->|<-1B->|

e.g. <code>(013612345678BR00080524A2232.9806N11304.9355E000.1101241323.8700000000L000450AC)</code>

1. <code>(</code>: Head
2. <code>013612345678</code>: Device ID
3. <code>BR00</code>: Command
4. <code>080524A2232.9806N11304.9355E000.1101241323.8700000000L000450AC</code>: GPS Data
5. <code>)</code>: Tail

#Alarm Packet Request (Device to Server)

    +------+-----------+------+------------+---------------------+------+
    | Head | Device ID | CMD  | Alarm Type | GPS Data            | Tail |
    +------+-----------+------+------------+---------------------+------+

    |<-1B->|<- 12B   ->|<-4B->|<-1B      ->|<-60B              ->|<-1B->|   

e.g. <code>(013612345678BO01x080524A2232.9806N11304.9355E000.1101241323.8700000000L000450AC)</code>

1. <code>(</code>: Head
2. <code>013612345678</code>: Device ID
3. <code>BO01</code>: Command
4. <code>x</code>: Alarm type, could be (0-7)

    0 - Power Off

    1 - Accident

    2 - SOS

    3 - Antitheft

    4 - Low speed

    5 - Overspeed

    6 - Out of geofence

    7 - Movement Alert

5. <code>080524A2232.9806N11304.9355E000.1101241323.8700000000L000450AC</code>: GPS Data
6. <code>)</code>: Tail 

#Alarm Response Packet (Server to Device)

    +------+-----------+------+------------+------+
    | Head | Device ID | CMD  | Alarm Type | Tail |
    +------+-----------+------+------------+------+

    |<-1B->|<- 12B   ->|<-4B->|<-1B      ->|<-1B->|

e.g. <code>(013612345678AS01x)</code>

1. <code>(</code>: Head
2. <code>013612345678</code>: Device ID
3. <code>AS01</code>: Command
4. <code>x</code>: Alarm type, could be (0-7)

    0 - Power Off

    1 - Accident

    2 - SOS

    3 - Antitheft

    4 - Low speed

    5 - Overspeed

    6 - Out of geofence

    7 - Movement Alert

5. <code>)</code>: Tail


#Handshake Request Packet (Device to Server)

    +------+-----------+------+-----------------+------+------+
    | Head | Device ID | CMD  | 000 + Device ID | HSO  | Tail |
    +------+-----------+------+-----------------+------+------+

    |<-1B->|<- 12B   ->|<-4B->|<-15B          ->|<-3B->|<-1B->|
 
e.g. <code>(013612345678BP05000013612345678HSO)</code>

1. <code>(</code>: Head
2. <code>013612345678</code>: Device ID
3. <code>BP05</code>: Command
4. <code>000013612345678</code>: 000 + Device ID
5. <code> HSO </code>: Hanshake request literal
6. <code>)</code>: Tail

#Handshake Response Packet (Server to Device)
    
    +------+-----------+------+------+------+
    | Head | Device ID | CMD  | HSO  | Tail |
    +------+-----------+------+------+------+

    |<-1B->|<- 12B   ->|<-4B->|<-3B->|<-1B->|

e.g. <code>(013612345678AP01HSO)</code>

1. <code>(</code>: Head
2. <code>013612345678</code>: Device ID
3. <code>AP01</code>: Command
4. <code>HSO</code>: Handshake literal
5. <code>)</code>: Tail

#GPS Data format

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

#Communication to the application server
The data is collected and posted to the application server, over HTTP connection the details could be configured in server.py. Data is posted in a fixed interval of time and a thread safe Queue is used for holding the array of datapackets for the required duration.

Note: a timeout of 2seconds has been defined hence if the webserver doesn't ACK the request between 2 seconds, connection will be terminated from the data server end.

The data is posted in a JSON body of the requested HTTP request which should of the following format:

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

a special attribute "packet\_type" has been added to identify and differentiate the different types of the packets which are:

1. <code>DNRML</code>: Normal data packet. 
2. <code>LOGIN</code>: Data from a Login/Enrolment request packet.
3. <code>ALARM:x</code>: Data from a alarm packet, where x after colon(:) represents the respective alarm type as per the TK103 protocol.

#Usage
1. Configure the settings in conf.py
2. Start the server as:
    ./server.py start
3. Stop the server as:
    ./server.py stop

Note: To monitor the server activity you may check tk103.log file.

#To do
1. Handle the other msgs
