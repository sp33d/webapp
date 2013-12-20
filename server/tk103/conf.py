"""
    A TCP port where server should listen.    
"""
LPORT = 8080

"""
    A HTTP url where data is to be sent.
"""
POST_TO_URL = "http://198.199.77.126/dashboard/api/"

"""
    Time(In seconds) for buffer the packet.
"""
WAITING_TIME = 5           

"""
    Time(in seconds) after which the connection with the client,
    will be dropped if last comminication exceeds the timeout.
"""
CLIENT_TIMEOUT = 180


"""
    Time(in seconds) after which connection with the application server
    will be dropped, if its response takes more timeout specified.
"""
APP_SERVER_TIMEOUT = 2
