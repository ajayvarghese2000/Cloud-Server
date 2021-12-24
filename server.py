#
#  ______ _           _       _____                 _          
# |  ____| |         | |     / ____|               (_)         
# | |__  | | __ _ ___| | __ | (___   ___ _ ____   ___  ___ ___ 
# |  __| | |/ _` / __| |/ /  \___ \ / _ \ '__\ \ / / |/ __/ _ \
# | |    | | (_| \__ \   <   ____) |  __/ |   \ V /| | (_|  __/
# |_|    |_|\__,_|___/_|\_\ |_____/ \___|_|    \_/ |_|\___\___|
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
#   2 ) Receive Sensor Data (POST)
#           (POST) Allows the server to receive and store the data from all the sensors from the
#                  drone. This is stored as a JSON document with the name of the registered drone
#                  as the access name
#           (GET)  Needs a drone access name; allows to see the sensor data that has been submitted
#   3 ) Receive AI cam feed (POST)
#           (POST) Allows the server to receive the AI cam feed from the drone
#           (GET)  Needs a drone access name; shows the AI cam feed
#   4 ) Receive Thermal cam feed 
#           (POST) Allows the server to receive the thermal cam feed from the drone
#           (GET)  Needs a drone access name; shows the thermal cam feed
#
# Written by Team CCC
#

## [Imports]
import flask
# Main components from the Flask framework to accept and send data 
from flask import Flask, jsonify, request, Response
import json
import requests
# Used for logging requests from the server
import logging

# Making sure the file won't be run directly from the python file
# To run the file you must first deploy it onto a guicorn server
app = Flask(__name__)

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)


@app.route('/')
def main():
    return 'Looks like you\'re lost'


