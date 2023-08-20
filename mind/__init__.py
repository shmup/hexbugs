import asyncio
import sqlite3
import json
from websockets.server import serve

def add_player(name):
    conn = sqlite3.connect('hexbugs.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO players (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()

async def handle_message(websocket, path):
    print(path)
    async for message in websocket:
        data = json.loads(message)
        if data['type'] == 'join':
            add_player(data['name'])
            await websocket.send('Player joined')
        elif data['type'] == 'concede':
            pass
        elif data['type'] == 'add_bug':
            pass
        elif data['type'] == 'move_bug':
            pass
        elif data['type'] == 'chat':
            pass

async def main():
    async with serve(handle_message, "localhost", 8765):
        print("Mind awakes.")
        await asyncio.Future()


if __name__ == '__main__':
    asyncio.run(main())

