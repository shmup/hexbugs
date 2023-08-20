import asyncio
import sqlite3
import json
from websockets.server import serve

class DBHandler:
    def __init__(self, db_name):
        self.db_name = db_name
        self.init_db()

    def init_db(self):
        with self:
            with open('schema.sql', 'r') as f:
                self.cursor.executescript(f.read())

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        _ = exc_type, exc_val, exc_tb  # are you happy pyright
        self.conn.commit()
        self.conn.close()

def add_player(name):
    with DBHandler('hexbugs.db') as cursor:
        cursor.execute("INSERT INTO players (name) VALUES (?)", (name,))

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
        print("The Mind awakes...")
        await asyncio.Future()


if __name__ == '__main__':
    asyncio.run(main())

