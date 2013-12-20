#!/usr/bin/env python

import sys, time
from daemonizer import Daemon
import logging

import conf
import handler

logger = logging
logger.basicConfig(filename='daemon.log',level=logging.ERROR)

class Server(Daemon):
    def run(self):
        handler.setup()
        while True:
            try:
                handler.loop()
                #time.sleep(1)
            except Exception, err:
                logger.error('Deamon: '+str(err))
                pass

if __name__ == "__main__":
    daemon = Server('/tmp/pt100-' + str(conf.LPORT) + '-daemon.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)
