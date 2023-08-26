import asyncio
import json
from websockets.server import serve
from hexbugs.mind.models import Game, Player
from hexbugs.mind.database import Session
from hexbugs.mind.manager import GameManager
from hexbugs.config import Config


def add_player(name):
    session = Session()
    player = Player(name=name)
    session.add(player)
    session.commit()


def update_game_state(game_id, state):
    session = Session()
    game = session.query(Game).filter_by(id=game_id).first()

    if game is None:
        raise ValueError(f"No game found with id: {game_id}")

    game.state = state
    session.commit()


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
    gm = GameManager()
    async with serve(gm.handle_message, Config.HOST, Config.PORT):
        print("The Mind awakes...")
        await asyncio.Future()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Restarting server')
