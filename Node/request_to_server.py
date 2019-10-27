from twisted.internet import task
from twisted.internet import reactor

timeout = 5.0 # Sixty seconds

def doWork():
    #do work here
    print('xxx')
    pass

l = task.LoopingCall(doWork)
l.start(timeout) # call every sixty seconds



reactor.run()
