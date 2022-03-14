#
# ______        _    ___  ______ _____      _____                 _          
# |  ___|      | |  / _ \ | ___ \_   _|    /  ___|               (_)         
# | |_ __ _ ___| |_/ /_\ \| |_/ / | |______\ `--.  ___ _ ____   ___  ___ ___ 
# |  _/ _` / __| __|  _  ||  __/  | |______|`--. \/ _ \ '__\ \ / / |/ __/ _ \
# | || (_| \__ \ |_| | | || |    _| |_     /\__/ /  __/ |   \ V /| | (_|  __/
# \_| \__,_|___/\__\_| |_/\_|    \___/     \____/ \___|_|    \_/ |_|\___\___|
#
#
# This framework will receive all data from the drones and handle data request
# from the client.
#
# It follows the REST API architectural style HTTP Requests are sent to the
# framework and responces are sent out in a JSON format.
# Main Endpoints:
#   1 ) Register a new drone (POST) / (GET)
#           (POST) Allows a drone to be added to the database and be set as active or inactive
#           (GET)  Lists all the available drones in the system currently and their data URLS
#   2 ) Receive data (POST)
#           (POST) Allows for drones to send data about the sensors on board and the video frames
#   3 ) Get Data (Websocket)
#           (Websocket) Allows for a client to connect to the server and stream data from a drone
#
# Written by Team CCC
#

## [Imports]
from fastapi import FastAPI                         # Used to create and run the FastAPI service
from fastapi.responses import RedirectResponse      # Used to display static html files i.e dashboard
from fastapi.staticfiles import StaticFiles         # Used to mount static directories
from fastapi.middleware.cors import CORSMiddleware  # Used to set CORS
import json                                         # Used to parse and analyse data received
import uvicorn                                      # The ASGI that will run the service
import socketio                                     # Used to create and run the SocketIO service
from subprocess import Popen                        # Used to Open the SSL version of the server

# Creating the FastAPI Server object
app = FastAPI()

# Creating the SocketIO Server object, setting CORS and increasing data limit to 10Mb and timeout intervals
sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins=[], ping_interval = (7200,7200), ping_timeout = 7200, max_http_buffer_size = 10000000)
socket_app = socketio.ASGIApp(sio)

# Opening the GUI as a file
html = open("static/index.html").read()

# Mounting the GUI onto the base URL
app.mount("/gui", StaticFiles(directory="Dashboard/src", html = True), name="GUI")

# Mounting the SocketIO Server to the '/ws' URL
app.mount("/ws", socket_app)

# Setting CORS for the FastAPI server
origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def redirect():
    response = RedirectResponse(url='/gui')
    return response

'''
# This is now a legacy method - It has been switched to a SocketIO method

############################## DO NOT USE ##############################

# URL for the drones to upload data to. Requires a drone name to be passed.
# See docs for the format in which the data is passed
@app.post("/uploaddata/{dname}")
async def uploaddata(dname, data : DataModel):
    
    # Creates/Opens the data file with the name of the drone
    with open('data/drones/' + dname + '.json', 'w') as buffer:

        # Dumps the data from the drone in a JSON format
        json.dump(data.dict(), buffer, indent=4)

        # Returns a success message
        return {"code" : 200 , "message" : "Success"}
'''

# URL to regsistar a new drone with the server, must send a drone ID
# All drone must do this before sending data over otherwise the GUI will
# not list the drone as accessible. 
@app.post('/drones/{dname}')
async def registarnewdrone(dname:int):

    # Loads the current list of drones
    with open('data/drones.json', "r") as old_f:

        # Attempts to read it as a JSON file
        try:

            # Loading the file as a JSON object
            old = json.load(old_f)

            # Creating the payload to be added to the file
            payload = {"id" : dname, "status" : 1}

            # Deleting any duplicates that may exist
            for i, data in enumerate(old["drones"]):
                if data["id"] == dname:
                    del old["drones"][i]

            # Adding the new Drone to the list
            old["drones"].append(payload)

            # Writing the updated data to the file
            with open('data/drones.json', "w") as new_f:
                json.dump(old, new_f, indent=4)

            # Returns a success message
            return {"code" : 200 , "message" : "Success"}
        
        # If the read fails, normally due to a race condition, server throws an error
        except:

            # Retuning the 500 error code
            return {"code" : 500 , "message" : "Internal Server Error, try again"}

# URL to remove a drone, must pass in the drone ID
# When the drone finishes it must remove it self from the active list
# The GUI will otherwise show a drone that isn't sending any data
@app.post('/removedrone/{dname}')
async def removedrone(dname:int):

    # Opens the list of drones registered
    with open('data/drones.json', "r") as old_f:

        # Attempts to read it as a JSON file
        try:

            # Loading the file as a JSON object
            old = json.load(old_f)
            
            # Deleting all entries with the drone ID supplied
            for i, data in enumerate(old["drones"]):
                if data["id"] == dname:
                    del old["drones"][i]
            
            # Writing the new data to the file
            with open('data/drones.json', "w") as new_f:
                json.dump(old, new_f, indent=4)
            
            # Returns a success message
            return {"code" : 200 , "message" : "Success"}
        
        # If the read fails, normally due to a race condition, server throws an error
        except:

            # Retuning the 500 error code
            return {"code" : 500 , "message" : "Internal Server Error"}

# URL to get the list of registered drones
# Will be used by the GUI to show the user what drones are connected
@app.get('/drones')
async def getdrones():

    # Opens the list of drones registered
    with open('data/drones.json', "r") as drones:
        
        # Attempts to read it as a JSON file
        try:
            # Loading the file as a JSON object
            data = json.load(drones)

            # Returns the data
            return data
        
        # If the read fails, normally due to a race condition, server throws an error
        except:

            # Retuning the 500 error code
            return {"code" : 500 , "message" : "Internal Server Error"}

# SocketIO handler for when a new client connects
@sio.on("connect")
async def connect(sid, env):
    
    # Prints a connection message and their session ID
    print("New Client connected ", sid)

# SocketIO handler for when a client disconnects
@sio.on("disconnect")
async def disconnect(sid):
    
    # Prints a disconnection message and their session ID
    print("Client disconnected ", sid)

# SocketIO handler for when a drone sends data
@sio.on("getdata")
async def getdata(sid, mes):

    # Gets the drone ID from the data to add a websocket label to emit to
    id = str(mes["dname"])

    # Debug statement to print what device id gave what message
    #print("New Data from " + id + " Received")

    # Forwarding the data sent by the drone to the correct label
    await sio.emit(id,mes)

'''
# Starting the uvicorn server
if __name__ == "__main__":
    kwargs = {"host": "0.0.0.0", "port": 80, "workers" : 1}
    kwargs.update({"debug": False, "reload": False})
    uvicorn.run("server:app", **kwargs)


'''
# Starting the uvicorn server on SSL mode
if __name__ == "__main__":
    Popen(['python3', '-m', 'https_redirect'])
    kwargs = {"host": "0.0.0.0", "port": 443, "workers" : 1, "ssl_keyfile" : "/etc/letsencrypt/live/ajayvarghese.me/privkey.pem", "ssl_certfile" : "/etc/letsencrypt/live/ajayvarghese.me/fullchain.pem"}
    kwargs.update({"debug": False, "reload": False})
    uvicorn.run("server:app", **kwargs)


