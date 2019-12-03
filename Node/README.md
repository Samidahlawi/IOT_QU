## NODE 
#paths
- for get the information of the node from client side
```
/device-info
```
- for read the data you sould send as this example 
path 
```
/readdata
```
JSON look like this when you try to read data
name_attatchment -> what sensor do your looking for
duration -> how long do you wanna read from the sensor
interval -> forEach period of time you wanna read ex for each 5 seconds read once 
```
{
	"name_attachment": "air quality sensor",
	"duration" : "60",
	"interval":"5"
}
```
*NOTE: remember duration and interval by seconds 

- ONLY SERVER Side use this path for check if node exist or not
```
/device
```