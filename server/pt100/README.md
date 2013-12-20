#A PT100 Server
PT100 is a proprietary communication protocol.
#Description
This is a very basic implementation of the PT100 protocol, to collect the GPS data and alarms in a optimal way.
altough much more optimization is pending.

this code is based on the https://github.com/durian/tk102-server
#Flow diagram of the Work of the server is
1. PT100 TCP server starts listening on a specified HOST and PORT.
2. PT100 client  connects to the server and sends the Enrollment/Login/Registration Packet.
    the communication can be graphically shown as:
    
    ```
    +-------------+                                                     +-------------+
    |   Server    |                                                     |   Client    |
    +-------------+                                                     +-------------+
    |                                                                                /|<------------+   
    |                                                                               / |             |   
    |<-------------------------------Feedback/Alaram Packet------------------------/  |\            |   
    |                                                                                 | \-----------+   
    |                                                                                 |
    ```

3. Terminate the server.

 
#Feedback Data Packet (Device to Server)
    SA200STTH;861001003125701;111;20131213;06:58:42;47F5;+28.486249;+77.61546;0;299.60;8;1;0000;11.30;0.000;0000000;1;0;0;0074

    ```
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
    ```

#Communication to the application server
The data is collected and posted to the application server, over HTTP connection the details could be configured in server.py. Data is posted in a fixed interval of time and a thread safe Queue is used for holding the array of datapackets for the required duration.

Note: a timeout of 2 seconds has been defined hence if the webserver doesn't ACK the request between 2 seconds, connection will be terminated from the data server end.

The data is posted in a JSON body of the requested HTTP request which should of the following format:

    [
    ]


#Usage
1. Configure the settings in conf.py
2. Start the server as:
    ./server.py start
3. Stop the server as:
    ./server.py stop

Note: To monitor the server activity you may check pt100.log file.
#To do
1. Handle the other msgs
