import asyncio
import json
from websockets.server import serve
from db import DBHandler, initialize_db


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
  initialize_db('hexbugs.db')
  async with serve(handle_message, "localhost", 8765):
    print("The Mind awakes...")
    await asyncio.Future()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Restarting server')
