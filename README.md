<p align="center">
	<a href="https://github.com/lboroWMEME-TeamProject/CCC-ProjectDocs"><img src="https://i.imgur.com/VwT4NrJ.png" width=650></a>
	<p align="center"> This repository is part of  a collection for the 21WSD001 Team Project. 
	All other repositories can be access below using the buttons</p>
</p>

<p align="center">
	<a href="https://github.com/lboroWMEME-TeamProject/CCC-ProjectDocs"><img src="https://i.imgur.com/rBaZyub.png" alt="drawing" height = 33/></a> 
	<a href="https://github.com/lboroWMEME-TeamProject/Dashboard"><img src="https://i.imgur.com/fz7rgd9.png" alt="drawing" height = 33/></a> 
	<a href="https://github.com/lboroWMEME-TeamProject/Cloud-Server"><img src="https://i.imgur.com/bsimXcV.png" alt="drawing" height = 33/></a> 
	<a href="https://github.com/lboroWMEME-TeamProject/Drone-Firmware"><img src="https://i.imgur.com/yKFokIL.png" alt="drawing" height = 33/></a> 
	<a href="https://github.com/lboroWMEME-TeamProject/Simulated-Drone"><img src="https://i.imgur.com/WMOZbrf.png" alt="drawing" height = 33/></a>
</p>

<p align="center">
	Below you can find buttons that link you to the repositories that host the code for the module itself. These can also be found linked in the collection repository: <a href="https://github.com/lboroWMEME-TeamProject/Drone-Firmware">Drone Firmware</a>. 
</p>


<p align="center">
	<a href="https://github.com/lboroWMEME-TeamProject/Main-Pi"><img src="https://i.imgur.com/4knNDhv.png" alt="drawing" height = 33/></a> 
	<a href="https://github.com/lboroWMEME-TeamProject/EnviroSensor"><img src="https://i.imgur.com/lcYUZBw.png" alt="drawing" height = 33/></a> 
	<a href="https://github.com/lboroWMEME-TeamProject/Geiger-Counter"><img src="https://i.imgur.com/ecniGik.png" alt="drawing" height = 33/></a> 
	<a href="https://github.com/lboroWMEME-TeamProject/Thermal-Camera"><img src="https://i.imgur.com/kuoiBTc.png" alt="drawing" height = 33/></a> 
	<a href="https://github.com/lboroWMEME-TeamProject/ai-cam"><img src="https://i.imgur.com/30bEKvR.png" alt="drawing" height = 33/></a>
</p>


------------

# Cloud-Server
A service that will be deployed on cloud infrastructure to accept data from drones and send data to the dashboard for users to view.

<p align="center">
	<img src="https://user-images.githubusercontent.com/58085441/147615433-53433adc-a942-4ddc-8246-a384917a6676.png"/>
</p>

This server is using a Uvicorn ASGI, FastAPI for it's framework and SocketIO to handle websocket connections.

Full documentation for those services can be found at the links below:
- [Uvicorn](https://www.uvicorn.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [SocketIO](https://python-socketio.readthedocs.io/en/latest/)

------------

## Table of Contents

- [Installation](#Installation)
- [Deployment](#Deployment)
    - [Systemctl Service](#systemctl-service)
- [API Endpoints](#api-endpoints)
    - [HTTP Endpoints](#http-endpoints)
        - [GUI](#get------gui)
        - [Return Drone List](#get---drones---gets-the-drones)
            - [Return Schema](#return-schema)
        - [Registers New Drone](#post---dronesdname---registers-a-new-drone)
            - [Return Schema](#return-schema-1)
        - [Removes a Drone](#post---removedronedname---removes-a-drone)
            - [Return Schema](#return-schema-2)
    - [SocketIO Event Listeners](#socketio-event-listeners)
        - [Connect](#connect---happens-on-a-new-connection)
        - [Disconnect](#disconnect---happens-on-a-disconnect)
        - [Getdata](#getdata---when-a-drone-sends-new-data)
            - [Data Packet Schema](#data-packet-schema)
            - [Base64 Encoded Images](#what-are-base64-encoded-images)
        - [What is a Websocket](#what-is-a-websocket)
- [Test Plan](#Test-Plan)

------------

## Installation
First clone the repository to a directory on your system. If you have git installed you can use the following command.
```
git clone https://github.com/lboroWMEME-TeamProject/Cloud-Server.git
```
This program is written in python 3, if you don't have it installed download it from the [python website](https://www.python.org/downloads/).
Once python is installed open up a terminal in the directory you cloned the repository and install the dependencies required using pip. It is recommended to use a python virtual environment to avoid conflicts.

To install all the required dependencies run the following command.

```
pip install -r requirements.txt
```

------------

## Deployment
As this is a server for production is it best to deploy the code in a data centre. However, for testing purposes running the `server.py` file will launch a local instance that can be used for development.

To configure the deployment open the `server.py` file and edit the following:
```
# Starting the uvicorn server
if __name__ == "__main__":
    kwargs = {"host": "0.0.0.0", "port": 80, "workers" : 4}
    kwargs.update({"debug": False, "reload": False})
    uvicorn.run("server:app", **kwargs)
```
Here you can change/add variables to the uvicorn instance.

`host` Allows you to bing the server to an IP address, `0.0.0.0` binds the server to all available IP's.

`port` Allows you to select what port to bind the server to.

`workers` Allows you to create multiple instances of the server to handle load management. 

For a full list of available options refer to the [uvicorn deployment docs](https://www.uvicorn.org/deployment/)

### Systemctl Service
If deploying on a cloud linux server it is recommended to create a Systemctl service to autostart and manage the server, an example systemctl startup script is supplied below.
```
[Unit]
Description=Uvicorn instance to serve cloud-server
After=network.target

[Service]
User=<User To Run>
Group=<Group User Belongs to>
WorkingDirectory=<Working directory>
ExecStart=python3 server.py

[Install]
WantedBy=multi-user.target
```
For a real production, it is recommended to put the uvicorn service behind an NGINX reverse-proxy and a CDN to take advantage of caching and DDOS protection.

----

## API Endpoints
This server has 2 types of endpoints, the HTTP request endpoints and the SocketIO listen events.

The server comes with a utility to test out the HTTP request endpoints. To view it start the server by running the `server.py` file then navigate to `http://<serverip:port>/docs` you will then be able to interact with all the HTTP endpoints there.

<p align="center">
	<img src="https://user-images.githubusercontent.com/58085441/147617034-e7fb1d03-2830-4c2b-9b57-7a9ae82ce6bd.gif"/>
</p>

----


### HTTP Endpoints
#### [GET] - / - GUI
This is the root endpoint, it will allow the user to see and interact with the dashboard, it returns a HTML page

<p align="center">
	<img src="https://github.com/lboroWMEME-TeamProject/Dashboard/raw/main/docs/img/Dashbaord%20Login.gif?raw=true"/>
</p>

#### [GET] - /drones - Gets the drones
This endpoint returns the list of drones currently registered onto the server. It is used by the dashboard to show the user what drones are currently connected
##### Return Schema
It returns a JSON object in the following form:
```
{
    "drones": [             # Array of active drones
        {
            "id": int,      # ID of the drone
            "status": int   # Status of the drone, 0 is in active 1 is active
        },
        ...                 # More JSON objects for each drone connected
    ]
}
```

#### [POST] - /drones/{dname} - Registers a new drone
This endpoint allows a new drone to be added to the server. You must supply a drone name which should be an positive integer. It is used by the drones to register themselves onto the server.
##### Return Schema
It returns a JSON object in the following form:
```
{
    "code": int,            # Event code 200 is success 500 is a internal failure
    "message": "string"     # Event Message
}
```

#### [POST] - /removedrone/{dname} - Removes a drone
This endpoint allows a drone to be removed from the server. You must supply a drone name which should be an positive integer. It is used by the drones to remove themselves frome the active list in the server.
##### Return Schema
It returns a JSON object in the following form:
```
{
    "code": int,            # Event code 200 is success 500 is a internal failure
    "message": "string"     # Event Message
}
```

----


### SocketIO Event Listeners
This server also uses SocketIO websockets for communication. Once a client has registered it can continuously send and receive data by listening on specific sockets.

#### [connect] - Happens on a new connection
This listener will print to the console when a new client has connected to the server.

#### [disconnect] - Happens on a disconnect
This listener will print to the console when a client has disconnected to the server.

#### [getdata] - When a drone sends new data
This listener takes the data packet that the drone sends, pulls the drone ID from it, then echo's the data packet to connected clients listening on the websocket with the drone ID.

##### Data Packet Schema
The data the drone sends must follow the following schema. Its is a JSON packet. ([What is JSON?](https://www.w3schools.com/whatis/whatis_json.asp))

```
{
	"dname": int, 		# The ID of the drone that is registered on the server
	"temp": float,		# The value of the temperature sensor
	"pressure": float,	# The value of the pressure sensor
	"humidity": float,	# The value of the humidity sensor
	"lux": float,		# The value of the light sensor
	"geiger": int,		# The value of the geiger counter
	"gas": {		# Sub-object to hold the values from the gas sensor
		"co": float,	# The Carbon Monoxide reading from the gas sensor
    		"no2": float,	# The Nitrogen Dioxide reading from the gas sensor
    		"nh3": float	# The Ammonia reading from the gas sensor
  	},
  	"air": {		# Sub-object to hold the values from the particulates sensor
    		"pm1": float,	# The value of PM1 particulates in the air
    		"pm2_5": float,	# The value of PM2.5 particulates in the air
    		"pm10": float	# The value of PM10 particulates in the air
  	},
  	"gps": {		# Sub-object to hold the values from the GPS sensor
    		"lat": float,	# The latitudinal position of the drone
    		"long": float	# The longitudinal position of the drone
  	},
  	"cam": base64,		# The image from the object-detection camera base64 encoded
  	"tcam": base64		# The image from the thermal camera base64 encoded
	"person" : bool		# See if a person was detected or not
}
```
Most of the data in the data packet is self-explanatory with exception of the base64 encoded images.
##### What are base64 encoded images?
The images that are received from the cameras on the drones will be raw binary data. 

The dashboard needs the newest frame from the drone to display to the user however, if we send the raw binary data in the data packet, it would make the size of the packet very large, hard to read and, longer to parse through.

base64 encoding takes the raw binary data and encodes it in base64, this gives a much smaller string that can be inserted into the data packet. [More on base64](https://en.wikipedia.org/wiki/Base64)

The best way to send the camera feeds would be to encode a video on the drone of the last few seconds then upload that chuck to the server just like how YouTube and Twitch work. This way, you can take advantage of modern video compression algorithms to make the data as small as possible.

However that would not be good for this use case as:

1. The hardware the drone firmware is deployed on is not very powerful. Having to encode a video as well as run object-detection and getting values from sensors will overwhelm it.
2. It would increase the latency as the server will have to first wait for the chuck to be encoded, then uploaded.

Base64 does have its disadvantages, namely that it take about 33% more resources to encode and decode when compared to binary data. However, most modern devices will be able to handel that increase without issue.
#### What is a websocket?
When sending data between a server and client there are a few options on how that can be done. 

The common way is to continually ping the server using a HTTP request with new data. This is ok for small amounts of data and when you are not interested in a real-time response.

<p align="center">
	<img src="https://user-images.githubusercontent.com/58085441/147609412-9e345cd1-a7ac-4e0e-b510-7f1388b9c068.gif" height=200/>
</p>

However, when it comes to real-time communication, this is a bad choice as it acts like a shot-gun sending data randomly with no regard for when it gets processed or if the server is overwhelmed. This is especially the case when you are sending large amounts of data over a short amount of time.

Furthermore, with HTTP requests there is additional overhead as each request must be handled by the server. 

If you want to send data real-time, a good method is to open a websocket on the server. This acts like a queue the drone can send data continuously to. This eliminates the extra overheads with HTTP request as once the websocket is open not additional handling of the data is done.

Then when the server is ready is can load the queue and process however it wants.
<p align="center">
	<img src="https://user-images.githubusercontent.com/58085441/147597894-db29d4ec-ee9f-4362-91dc-f7d4878dd6e9.gif" height=200/>
</p>

As the data from the drone needs to be shown in real-time once the drone registers a websocket is opened that it can send data to.

## Test Plan

<div align="center">

|Objective|Testing Strategy|Expected Output|Current Output|Pass/Fail|
|--|--|--|--|:--:|
|Show the GUI when a user visits the home URL `/`|Use a web browser to visit the home URL and observe the result|The dashboard should be shown and the user should be prompted to login|The dashboard is shown and the user is prompted to login|:heavy_check_mark:|
|Return a JSON object filled with the drones that are currently connected to the server when a GET request is processed on the `/drones` endpoint|Use the built-in API endpoint tester to send a GET request to the server and observer the result|The server should return a JSON object with the ID's of the drones connected to the server at any given point|The server does return a JSON object of the drones connected to the server|:heavy_check_mark:|
|Needs to add a new drone to the list of drones connected when a new drone connects to the server using the API endpoint ` /drones/{dname}`|Use the simulated drone tool to register itself with the server, then verify it's successes using the `/drones` API endpoint.|The server should return a JSON object indicating if it could successfully add a new drone to the connected drone list or not.|The Server returns a JSON object with a 200 status code indicating a success which can be verifiable using the `/drones` endpoint or the GUI.|:heavy_check_mark:|
|Needs to remove a drone from the list of connected drones when a drone disconnects using the API endpoint `/removedrone/{dname}`|Us the simulated drone tool to disconnect from the server, then verify it's successes using the `/drones` API endpoint.|The server should return a JSON object indicating if it could successfully remove the drone from the connected drone list or not.|The Server returns a JSON object with a 200 status code indicating a success which can be verifiable using the `/drones` endpoint or the GUI.|:heavy_check_mark:|
|Open a websocket with the drones ID when a drone connects and emmit the data the drone sends to the server to that websocket|Use the simulated drone tool to connect to and send data to the server then listen to the response on the websocket with the drone ID to see if the server echoes the data sent back.|The console of the simulated drone should display the data it sent to the server/The data should be shown on the GUI|The console does echo the data the drone sent and the GUI does show the data.|:heavy_check_mark:|

</div>