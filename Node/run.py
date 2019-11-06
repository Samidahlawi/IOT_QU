from flask import Flask, request
from flask_restful import Resource, Api
from datetime import datetime
from config import ConfigAddress
from attachments import Attachment
from ANSI_escape import bcolors
import requests, time, json, pprint
from background_thread import RepeatedTimer
from time import sleep
from threading import Timer

app = Flask(__name__)
api = Api(app)

###############
## paths
# /devise_Info => to get the information of the device and what device have of attchements 
# /device/readdata => 
###############

### temporary variables 
first_time_run = True
set_time = ''
# class of main server
class Server():
  def __init__(self,ip,port):
	self.ip = ip # The IP of the server
	self.port = port # which port the server is running right-now


########### START GLOBAL VARIABLES  && FUNCTIONS #########################
# SEREVR information (controller)
		# ip 	,      port
server = Server('192.168.1.2','3000')


# ATTACHMENTS HERE
all_attachment = ['air quality sensor','temperature sensor', 'humidity sensor'] 

configuration = ConfigAddress()
# setup the NODE information
node = {
 "ip_address":configuration.get_ip_address(),
 "id":configuration.get_mac_address('wlan0'), # wlan0 for interface of wifi in the raspberryPi
 "start":datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
 "attachments":all_attachment,
 "power_supply":"Battery",
 "device_type":"Raspberry PI",
 "port":'9090'					# which port the current node run on it
}

print(bcolors.UNDERLINE + '>>##################################START RUN NODE#####################################' + bcolors.ENDC)
pprint.pprint(node)
print(bcolors.UNDERLINE + '>>#####################################################################################' + bcolors.ENDC)

#########
# RUNCTION TO GET THE IP EACH PERIOD OF TIME && DO THE REQUEST TO THE SERVER IF THE IP != 'UNDEFINED'
# HERE WE'RE GOING TO MAKE SURE WE CONNECTED WITH SERVER
# WE'RE USING SCEDULER TO EXCTE THE FUNCTION PERIOD OF TIME FOREXAMPLE EACH 5 MINUTES 
# HOW MANY MINUTES DO YOU WANT TO WAIT TO GET IP AND MAKE THE REQUEST TO MAIN SERVER !!
##### UpTODate for IP and Request to Main SERVER 
def up_to_date():
    node['ip_address'] = ConfigAddress().get_ip_address()
    if (node['ip_address'] != 'undefined'):
    	#register_node()
	#print('Requesting to server')
	try:
	  r = requests.post('http://'+server.ip+':'+server.port+'/nodes/device-registry', json=node)
	  res = json.loads(r.text)
	  if str(res['state']) == 'exist': # when the response become as exist node so we're going to do update request for update the data in the server
	    	try:
				update = requests.patch('http://'+server.ip+':'+server.port+'/nodes/'+ node['id'] ,json=node)
				print(bcolors.OKBLUE + '****** SUCCESSFULLY UPDATED ******')
				print('>> THE NODE UP-TO-DATE in the server' + bcolors.ENDC)
				clean_up()
			except:
		 	    print(bcolors.FAIL + ">> Cann't UPDATE THE NODE !!" + bcolors.ENDC) 
	  else:
		print(bcolors.OKGREEN + '****** SUCCESSFULLY REGISTERED ******')
		print('>> THE NODE registered successfully ...' + bcolors.ENDC)
		clean_up()
	except:
		  print(bcolors.WARNING  + "****** WORNING ******" + bcolors.ENDC)
      	  print(bcolors.FAIL + ">> Invild request to main SERVER, sorry cann't resgister the node to device-registry, make sure the main server is running!!, and try to restart the node" + bcolors.ENDC)
    else:
        print(bcolors.UNDERLINE + "YOU'RE NOT CONNECTING TO WIFI :( " + bcolors.ENDC)

## make rt global to access everyweher
rt = ''
second = 10
def background_thread():
	global rt, second
	rt = RepeatedTimer(second, up_to_date) # it auto-starts, no need of rt.start()
	try:
    	  sleep(31556952) # your long-running job goes here...
	except:
	  print('ONE YEAR $_$')
	#finally:
	#  rt.stop()

#### CLEANUP function to close the background-thread 
def clean_up():
   global rt
   try:
	rt.stop()
   	print(bcolors.OKGREEN + 'Finally, Killed background thread D:' + bcolors.ENDC)
   except:
	print('no background thread')
##########  END  GLOBAL VARIABLES && FUNCTION  ##################



# This class for request and response for device information 
class DeviceInfo(Resource):
	# function will return json about informatin of device 
	def get(self):
		global node
		return node,200


# This class for receive the request from the main serever to check if the current node is dead or alive
class CheckDevice(Resource):
	# it's a normal function with return all the information of the current node
	def get(self):
		global node, set_time
		try:
			clean_up()
		finally:
			node['ip_address'] = ConfigAddress().get_ip_address()
			set_time = time.time()
			t = Timer(10,self.is_node_connect_to_server)
			t.start() # after 10 seconds, is_node_connect_to_server
			return node,200

	def is_node_connect_to_server(self):
		global set_time, thread_killed
		if ((time.time() - set_time) > 10): ## after 10 seconds if the server not send any request will call background_thread function
		   set_time = time.time()
		   print(bcolors.FAIL + 'Looking for the server.../' + bcolors.ENDC)
		   background_thread()
		else:
		   print(bcolors.OKGREEN + 'THE NODE AND SERVER CONNECTED *_* ' + bcolors.ENDC)


# This class for read data from sensor node
class ReadData(Resource):
	def post(self):
		global all_attachment
		body = request.json

		name_of_attachment = str(body['name_attachment']).upper()
		duration = int(body['duration'])
		interval = int(body['interval'])
		results  = []
		timestamp = int(time.time())
		#print(type(duration), type(name_of_attachment), type(interval))
		#print(isinstance(duration,int) and isinstance(interval,int) and isinstance(name_of_attachment,str))
		if isinstance(duration,int) and isinstance(interval,int) and isinstance(name_of_attachment,str) :
		 if name_of_attachment == 'AIR QUALITY SENSOR':
		   while True:
			time.sleep(interval)
			sensor = Attachment()
			results.append(sensor.air_quality_sensor()) # there is a paramter 'pin' if you would like to change the pin 
			if int(time.time() - timestamp) >= duration*60:
				print(bcolors.OKGREEN + '>>Done ^_^ ')
				print(results)
				print(' ' + bcolors.ENDC)
				return {'results':results,'number_of_result':len(results)}, 200


     		 if name_of_attachment == 'TEMP SENSOR':
			pass
		 else:
			return {'Message':'The attachment not exist','My Attachments':all_attachment}

		else:
		  return {'Error':'[error]'},204

# DEFINE PATH 
# GET - /device-info => to get details of the device
api.add_resource(DeviceInfo,'/device-info')
# GET - /device => return information of the current node used 'ONLY'** WITH THE SERVER. SO ONLY THE SERVER USED THIS PATH ****IMPORTANT 
api.add_resource(CheckDevice,'/device')
# POST - /readdata 
api.add_resource(ReadData,'/readdata')


### DEVICE REGISTRY
class Registry():
	# Make a request to the device-registry in the main server and send the object of node to save it in the database of the server
  def register_node(self):
    global rt
    try:
	r = requests.post('http://'+server.ip+':'+server.port+'/nodes/device-registry', json=node)
	res = json.loads(r.text)
	if str(res['state']) == 'exist': # when the response become as exist node so we're going to do update request for update the data in the server
		try:
		  update = requests.patch('http://'+server.ip+':'+server.port+'/nodes/'+ node['id'] ,json=node)
		  print(bcolors.OKBLUE + '****** SUCCESSFULLY UPDATED ******')
		  print('>> THE NODE UP-TO-DATE in the server' + bcolors.ENDC)
	    except:
		  print(bcolors.FAIL + ">> Cann't UPDATE THE NODE !!" + bcolors.ENDC) 
	else:
		print(bcolors.OKGREEN + '****** SUCCESSFULLY REGISTERED ******')
		print('>> THE NODE registered successfully ...' + bcolors.ENDC)
    except:
	  	print(bcolors.WARNING  + "****** WORNING ******" + bcolors.ENDC)
		print(bcolors.FAIL + ">> Invild request to main SERVER, sorry cann't resgister the node to device-registry, make sure the main server is running!!, and try to restart the node" + bcolors.ENDC)
		#print("request to the server when it's connecting")
		t = Timer(5,background_thread)
                t.start() # after 10 seconds, background_thread
# Call function of device registry to do request to the server and register the node in the database
start_registry = Registry()
start_registry.register_node()


print('>>' + bcolors.HEADER + bcolors.BOLD+'THE NODE IS RUNNING...*_*' + bcolors.ENDC)
## Start run the server Node
if __name__ == '__main__':
        try:
		app.run(host='0.0.0.0',port=node['port'])
	finally:
	  try:
		clean_up()
		t.cancel()
		print('SHUT DOWN...')
	  except:
		print('SHUT DOWN...')
