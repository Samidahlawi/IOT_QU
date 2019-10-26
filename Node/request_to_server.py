import sched, time
## HERE we're goint to make sure we connected with server
## WE're using scheduler to excute the function for period of time forexample each 5 minutes
s = sched.scheduler(time.time, time.sleep)
minute = 1   ## How many minutes do you want to wait to make request to the main SERVER

def connect_to_server(sc, checked): 
    print "Doing stuff..."
    # do your stuff
    s.enter(60*minute, 1, connect_to_server, (sc,))

s.enter(60*minute, 1, connect_to_server, (s,))
s.run()