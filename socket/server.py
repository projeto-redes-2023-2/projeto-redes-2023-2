import asyncio
import websockets

async def handle_client(websocket, path):
    while True:
        message = await websocket.recv()
        print(f"Received message: {message}")
        await websocket.send(f"Server received: {message}")

start_server = websockets.serve(handle_client, "projetoredes20232.unb.br", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()