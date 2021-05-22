import ssl
import pathlib
from websockets import client
import asyncio

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
cert = pathlib.Path(__file__).with_name("cert.crt")
key = pathlib.Path(__file__).with_name("key.pem")

ssl_context.load_cert_chain(cert, keyfile=key)

ssl_context.load_verify_locations(cert)

async def connection():
    uri = "wss://localhost:4242"

    async with client.connect(
        uri, ssl=ssl_context
    ) as websocket:
        async for message in websocket:
            print(message)

asyncio.get_event_loop().run_until_complete(connection())