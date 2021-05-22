# RaspberryPI Car
For school, code mainly copied from https://github.com/otaniemenlukio/projektit/tree/master/raspberry_car_PCA

## ./car.py
This file contains the defination of the Car object. The object contains all code required to drive the remote controlled car

## ./drive.py
Example of driving the car 

## ./server.py
Server for remote controlling the car via websockets

Connect to port 4242 of the raspberry driving the car and send control messages through the websocket:
Send:
* "f" to go forward
* "b" to go backward
* "l" to turn left
* "r" to turn right
* "q" to stop driving
* "s" to start driving
