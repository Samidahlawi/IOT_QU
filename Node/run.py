from flask import Flask, request
from flask_restful import Resource, Api
from datetime import datetime
from config import ConfigAddress
from attachments import Attachment
import requests, time, json

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


########### START GLOBAL VARIABLES ############
# SEREVR information
server = Server('192.168.1.2','3000')


# ATTACHMENTS HERE
all_attachment = ['air quality sensor','temperature sensor', 'humidity sensor'] 


# setup the node information
node = {
 "ip_address":ConfigAddress().get_ip_address(),
 "id":ConfigAddress().get_mac_address('wlan0'), # wlan0 for interface of wifi in the raspberryPi
 "start":datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
 "attachments":all_attachment,
 "power_supply":"Battery",
 "device_type":"Raspberry PI"
}

print('>>##################################START RUN NODE#####################################')
print(node)
print('>>#####################################################################################')
##########  END  GLOBAL VARIABLES ###########



# This class for request and response for device information 
class DeviceInfo(Resource):
	# function will return json about informatin of device 
	def get(self):
		global node
		return node,200


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
				print('>>done')
				print(results)
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
# POST - /readdata 
api.add_resource(ReadData,'/readdata')


### DEVICE REGISTRY
# Make a request to the device-registry in the main server and send the object of node to save it in the database of the server
def register_node():
    try:
	r = requests.post('http://'+server.ip+':'+server.port+'/nodes/device-registry', json=node)
	res = json.loads(r.text)
	if str(res['state']) == 'exist': # when the response become as exist node so we're going to do update request for update the data in the server
		try:
		  update = requests.patch('http://'+server.ip+':'+server.port+'/nodes/'+ node['id'] ,json=node)
		  print('****** SUCCESSFULLY UPDATED ******')
		  print('>> THE NODE UP-TO-DATE in the server')
	        except:
		  print(">> Cann't UPDATE THE NODE !!") 
	else:
		print('****** SUCCESSFULLY REGISTERED ******')
		print('>> THE NODE registered succssfully ...')
    except:
	print("****** WARNING ******")
	print(">> Invild request to main SERVER, sorry cann't resgister the node to device-registry, make sure the main server is running!!, and try to restart the node")

# Call function of device registry to do request to the server and register the node in the database
register_node()


print('RUNNING...')
## Start run the server Node
if __name__ == '__main__':
        app.run(host='0.0.0.0',port=9090)





