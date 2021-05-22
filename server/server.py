import asyncio
from os import write
import requests
from websockets import server, exceptions
from websockets.legacy.server import WebSocketServerProtocol
import ssl
import pathlib


from car import Car
car = Car()

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
cert = pathlib.Path(__file__).with_name("cert.crt")
key = pathlib.Path(__file__).with_name("key.pem")
ssl_context.load_cert_chain(cert, keyfile=key)

connCount = 0
async def carController(websocket: WebSocketServerProtocol, path: str):
    global connCount

    if connCount == 1:
        await websocket.send("Car is already being controlled")
        await websocket.close()
        return

    connCount = 1
    remoteIP = websocket.remote_address
    print(f"Websocket connection from: {remoteIP}")
    await websocket.send(str(car))
    try:
        async for message in websocket:
            if message == "f": # Forward
                car.forward()
            elif message == "b": # Backward
                car.backward()
            elif message == "l": # Left
                car.turnLeft()
            elif message == "r": # Right
                car.turnRight()
            elif message == "q": # Quit
                car.stopDriving()
            elif message == "s": # Start
                car.beginDriving()
            elif message == "c":
                car.centerSteering()
            else:
                await websocket.send("Unknown message")
            await websocket.send(str(car))
            car.updatePwm()
    except exceptions.ConnectionClosedError as e:
        car.stopDriving()
        connCount = 0
        return

async def main():
    ip = getIp()
    async with server.serve(carController, "localhost", 4242, ssl=ssl_context):
        print(f"Websocket server listening on address {ip}:4242")
        await asyncio.Future()



def getIp():
    return requests.get("https://api.ipify.org/").text
asyncio.run(main())
