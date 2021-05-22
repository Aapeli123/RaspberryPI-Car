from car import Car
import uuid
from bottle import route, run
import netifaces
car = Car()

sessionid = ""

@route('/start')
def start():
    global sessionid
    if sessionid != "":
        return "Car is already being controlled"
    sessionid = str(uuid.uuid4())
    return sessionid

@route('/f/<sid>')
def goForward(sid):
    global sessionid
    if sessionid == sid:
        car.forward()
        return str(car)

@route('/b/<sid>')
def goBackwards(sid):
    global sessionid
    if sessionid == sid:
        car.backward()
        return str(car)

@route('/l/<sid>')
def turnLeft(sid):
    global sessionid
    if sessionid == sid:
        car.turnLeft()
        return str(car)

@route('/r/<sid>')
def turnRight(sid):
    global sessionid
    if sessionid == sid:
        car.turnRight()
        return str(car)

@route('/s/<sid>')
def startDriving(sid):
    global sessionid
    if sessionid == sid:
        car.beginDriving()
        return str(car)

@route('/q/<sid>')
def stopDriving(sid):
    global sessionid
    if sessionid == sid:
        car.stopDriving()
        return str(car)


@route('/c/<sid>')
def centerSteering(sid):
    global sessionid
    if sessionid == sid:
        car.centerSteering()
        return str(car)


@route('/quit/<sid>')
def quit(sid):
    global sessionid
    if sid == sessionid:
        sessionid = ""
    return

def getIp():
    return netifaces.interfaces()["wlan0"]

print(f"Starting server on address: {getIp()}:4242")
run(host="0.0.0.0", port=4242)
