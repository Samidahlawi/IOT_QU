from flask import Flask, request
from flask_restful import Resource, Api
from datetime import datetime
from config import ConfigAddress
from attachments import Attachment

import time 


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

###########
# ATTACHMENTS HERE
all_attachment = ['air quality sensor','temperature sensor', 'humidity sensor'] 
##########

# This class for request and response for device information 
class DeviceInfo(Resource):
	# wlan0 for interface of wifi in the raspberryPi 
	address = ConfigAddress()
	mac_address = address.get_mac_address('wlan0')
	ip_address  = address.get_ip_address() 
	# function will return json about informatin of device 
	def get(self):
		global first_time_run, set_time, all_attachments

		if (first_time_run):
		    set_time  = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
		    first_time_run = False
		return {
			"ip_address":self.ip_address,
			"id":self.mac_address,
			"start_Run":set_time,
			"attachments":all_attachment,
			"power_supply":"Battery",
			"device_type":"Raspberry PI"
			},200

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
				print('done')
				print(results)
				return {'results':results,'number_of_result':len(results)}, 200


     		 if name_of_attachment == 'TEMP SENSOR':
			pass
		 else:
			return {'Message':'The attachment not exist','My Attachments':all_attachment}

		else:
		  return {'Error':'[error]'},204


# GET - /device_info => to get details of the device
api.add_resource(DeviceInfo,'/device_info')
# POST - /readdata 
api.add_resource(ReadData,'/readdata')


if __name__ == '__main__':
	app.run(host='0.0.0.0',port=9090)


