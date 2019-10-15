##### 
#####
import socket

class ConfigAddress:
  def get_mac_address(self,interface='eth0'):
  # Return the MAC address of the specified interface
   try:
     str = open('/sys/class/net/%s/address' %interface).read()
   except:
     str = "00:00:00:00:00:00"
   return str[0:17]
 
 # method to get the ip address of wichever the interface is used!!
  def get_ip_address(self):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

###
# This variable will get the MAC-address of wlan0 interface
# In the raspberry pi the interface of the wifi is called 'wlan0'
# interface_of_wlan0 = "wlan0"
# print(getMAC(interface_of_wlan0))
###
