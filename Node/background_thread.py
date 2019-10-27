from threading import Timer
from time import sleep

class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False


##### UpTODate for IP and Request to Main SERVER 
#def up_to_date():
#    print('xxxx')
#    
#rt = RepeatedTimer(3, up_to_date) # it auto-starts, no need of rt.start()
#try:
#     sleep(9)  # your long-running job goes here...
#     rt.start()
#finally:
#     rt.stop() # better in a try/finally block to make sure the program ends!


