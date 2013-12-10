#A TK103 Server
based on docs from http://location.io/files/2013/04/GPS-Tracker-Communication-Protocol.pdf
#Description
This is a very basic implementation of the TK103 pprotocol, to collect the GPS data and alarms in a optimal way.
altough much more optimization is pending.

this code is based on the https://github.com/durian/tk102-server
#Flow diagram of the Work of the server is
1. TK103 TCP server starts listening on a specified HOST and PORT.
2. TK103 client  connects to the server and sends the Enrollment/Login/Registration Packet.
    the communication can be graphically shown as:
    <code>
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
    </code>
3. Terminate the server.

#Login/Enrollment Request Packet (Device to Server)
    
    +------+-----------+------+-----------------+---------------------+------+
    | Head | Device ID | CMD  | 000 + Device ID | GPS Data            | Tail |
    +------+-----------+------+-----------------+---------------------+------+

    |<-1B->|<- 12B   ->|<-4B->|<-15B          ->|<-60B              ->|<-1B->|

    e.g.
    <code>(013612345678BP05000013612345678080524A2232.9806N11304.9355E000.1101241323.8700000000L000450AC)</code>
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

    e.g.
    <code>(013612345678AP05)</code>
    1. <code>(</code>: Head
    2. <code>013612345678</code>: Device ID
    3. <code>AP05</code>: Command
    4. <code>)</code>: Tail
 
#Feedback Data Packet (Device to Server)

    +------+-----------+------+---------------------+------+
    | Head | Device ID | CMD  | GPS Data            | Tail |
    +------+-----------+------+---------------------+------+

    |<-1B->|<- 12B   ->|<-4B->|<-60B              ->|<-1B->|

    e.g.
    <code>(013612345678BP05080524A2232.9806N11304.9355E000.1101241323.8700000000L000450AC)</code>
    1. <code>(</code>: Head
    2. <code>013612345678</code>: Device ID
    3. <code>BP05</code>: Command
    4. <code>080524A2232.9806N11304.9355E000.1101241323.8700000000L000450AC</code>: GPS Data
    5. <code>)</code>: Tail

#Alarm Packet Request (Device to Server)

    +------+-----------+------+------------+---------------------+------+
    | Head | Device ID | CMD  | Alarm Type | GPS Data            | Tail |
    +------+-----------+------+------------+---------------------+------+

    |<-1B->|<- 12B   ->|<-4B->|<-1B      ->|<-60B              ->|<-1B->|   

    e.g.
    <code>(013612345678BO01x080524A2232.9806N11304.9355E000.1101241323.8700000000L000450AC)</code>
    1. <code>(</code>: Head
    2. <code>013612345678</code>: Device ID
    3. <code>BO01</code>: Command
    4. <code>x</code>: Alarm type, could be (0-7)
    4.1 0 - Power Off
    4.2 1 - Accident
    4.3 2 - SOS
    4.4 3 - Antitheft
    4.5 4 - Low speed
    4.6 5 - Overspeed
    4.7 6 - Out of geofence
    4.8 7 - Movement Alert
    5. <code>080524A2232.9806N11304.9355E000.1101241323.8700000000L000450AC</code>: GPS Data
    6. <code>)</code>: Tail 

#Alarm Response Packet (Server to Device)

    +------+-----------+------+------------+------+
    | Head | Device ID | CMD  | Alarm Type | Tail |
    +------+-----------+------+------------+------+

    |<-1B->|<- 12B   ->|<-4B->|<-1B      ->|<-1B->|

    e.g.
    <code>(013612345678AS01x)</code>
    1. <code>(</code>: Head
    2. <code>013612345678</code>: Device ID
    3. <code>AS01</code>: Command
    4. <code>x</code>: Alarm type, could be (0-7)
    4.1 0 - Power Off
    4.2 1 - Accident
    4.3 2 - SOS
    4.4 3 - Antitheft
    4.5 4 - Low speed
    4.6 5 - Overspeed
    4.7 6 - Out of geofence
    4.8 7 - Movement Alert
    5. <code>)</code>: Tail


#Handshake Request Packet (Device to Server)

    +------+-----------+------+-----------------+------+------+
    | Head | Device ID | CMD  | 000 + Device ID | HSO  | Tail |
    +------+-----------+------+-----------------+------+------+

    |<-1B->|<- 12B   ->|<-4B->|<-15B          ->|<-3B->|<-1B->|
 
    e.g.
    <code>(013612345678BP05000013612345678HSO)</code>
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

    e.g.
    <code>(013612345678AP01HSO)</code>
    1. <code>(</code>: Head
    2. <code>013612345678</code>: Device ID
    3. <code>AP01</code>: Command
    4. <code>HSO</code>: Handshake literal
    5. <code>)</code>: Tail
    
#To do
1. Handle the other msgs
