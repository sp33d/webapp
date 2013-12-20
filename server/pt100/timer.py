import threading
import time

import conf

class TimerClass(threading.Thread):
   
    callback_function = None
    callback_fun_args = None

    def __init__(self, cf_fun, cf_fun_args):
        self.callback_function = cf_fun
        self.callback_fun_args = cf_fun_args
        threading.Thread.__init__(self)
        self.event = threading.Event()

    def run(self):
        while not self.event.is_set():
            if self.callback_function is not None:
                if self.callback_fun_args is not None:
                    self.callback_function(self.callback_fun_args)
                else:
                    self.callback_function()
            else:
                print "No callback routine defined, exiting"
                self.stop()
            self.event.wait( conf.WAITING_TIME )

    def stop(self):
        self.event.set()

def testcallback(item):
    print "Posting data", item
    item.append('1')

if __name__ == '__main__':
    
    this_is_a_test_var = []

    tmr = TimerClass(cf_fun=testcallback, cf_fun_args=this_is_a_test_var)
    tmr.start()

    time.sleep( 10 )

    tmr.stop()

    print this_is_a_test_var
