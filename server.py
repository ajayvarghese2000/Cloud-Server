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
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import json
import uvicorn
import socketio
from dataclass import DataModel


# Creating the FastAPI Server object
app = FastAPI()

# Creating the SocketIO Server object, setting CORS and increaing data limit to 10Mb
sio = socketio.AsyncServer(async_mode="asgi",cors_allowed_origins=[], max_http_buffer_size = 10000000)
socket_app = socketio.ASGIApp(sio)

# Opening the GUI as a file
html = open("static/index.html").read()

# Mounting the static folder onto the URL
app.mount("/static", StaticFiles(directory="static/", html = True), name="static")

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

# Displaying the GUI on load to the base domin
@app.get("/")
async def gui():
    # Returns the GUI that is loaded from html variable
    return HTMLResponse(html)

# URL for the drones to upload data to. Requires a drone name to be passed.
# See docs for the format in which the data is passed
@app.post("/uploaddata/{dname}")
async def uploadcam(dname, data : DataModel):
    
    # Creates/Opens the data file with the name of the drone
    with open('data/drones/' + dname + '.json', 'w') as buffer:

        # Dumps the data from the drone in a JSON format
        json.dump(data.dict(), buffer, indent=4)

        # Returns a success message
        return {"code" : 200 , "message" : "Success"}


@sio.on("connect")
async def connect(sid, env):
    print("New Client connected ", sid)

@sio.on("disconnect")
async def disconnect(sid):
    print("Client disconnected ", sid)


'''@sio.on("getframe")
async def getframe(sid,mes):
    data = loadframe(0)
    await sio.emit("BASE64SEND", data)
'''
'''def loadframe(d_name):
    with open("static/img/s.png", "rb") as pic:
        encoded = base64.b64encode(pic.read())
        encoded = encoded.decode("utf-8")
        return encoded

'''

if __name__ == "__main__":
    kwargs = {"host": "0.0.0.0", "port": 80}
    kwargs.update({"debug": False, "reload": False})
    uvicorn.run("server:app", **kwargs)



