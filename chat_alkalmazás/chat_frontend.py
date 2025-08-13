import json
import asyncio
import websockets

URL = "ws://127.0.0.1:8000/ws"

async def listen_messages(websocket):
    async for message in websocket:
        data = json.loads(message)
        print(data)
        print(type(data))
        if isinstance(data, list):
            for item in data:
                print(f"{item['username']}: {item['text']}")
        else:
            print(f"{data['username']}: {data['text']}")

async def send_message(websocket, username):
    loop = asyncio.get_event_loop()
    while True:
        text = await loop.run_in_executor(None, input)
        if text == "quit()":
            break
        await websocket.send(json.dumps({"username": username, "text": text}))

async def main():
    username = input("Enter username: ")
    async with websockets.connect(URL) as websocket:
        await asyncio.gather(
            listen_messages(websocket),
            send_message(websocket, username)
        )

if __name__ == "__main__":
    asyncio.run(main())