## SERVER


--------
## SETUP 
# First, make sure you install Mongodb
THEN Run these commands in the server folder
- Install npm 
```
install npm
```
- Install Axios
```
npm install axios
```
THEN 
- Start run the server
```
npm start
```
ENJOY (: 
--------


## PATHS FOR SERVER
- FOR GET ALL NODES
```
/nodes
```
- Then Server will return JSON array of objects like this one
Example
```
"nodes": [
        {
            "_id": "5de6b7bf3e5b9b2ebc03c2a8",
            "updatedAt": "2019-12-03T20:31:07.039Z",
            "createdAt": "2019-12-03T19:30:07.934Z",
            "port": "9090",
            "start": "03/12/2019 22:44:42",
            "device_type": "Raspberry PI",
            "ip_address": "192.168.1.3",
            "id": "b8:27:eb:5a:e3:4d",
            "power_supply": "Battery",
            "state": "on",
            "__v": 0,
            "attachments": [
                "air quality sensor",
                "temperature sensor",
                "humidity sensor"
            ]
        },
        {
            "_id": "5de6c3765ebb6f34f36029a5",
            "updatedAt": "2019-12-03T20:30:48.155Z",
            "createdAt": "2019-12-03T20:20:06.475Z",
            "port": "9090",
            "start": "03/12/2019 20:23:14",
            "device_type": "Raspberry PI",
            "ip_address": "192.168.1.4",
            "id": "b8:27:eb:7b:60:36",
            "power_supply": "Battery",
            "state": "on",
            "__v": 0,
            "attachments": [
                "air quality sensor",
                "temperature sensor",
                "humidity sensor"
            ]
        }
    ]
}

```

