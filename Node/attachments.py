# The Qassim University (QU)
# 
# (C) 2019
#

import time
import grovepi


## WE have to defined all the attachments we're going to use
my_attachments = ['air quality sensor','temperature sensor']

class Attachment:
 ## function for air quality
  def air_quality_sensor(self,pin = 0):
	self.air_sensor = pin
	grovepi.pinMode(self.air_sensor,"INPUT")
	try:
	  # Get sensor value
	  self.sensor_value = grovepi.analogRead(self.air_sensor)
          return self.sensor_value
	except IOError:
	  return "Error"


