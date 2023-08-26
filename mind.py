import asyncio
from websockets.server import serve
from hexbugs.services.manager import GameManager
from hexbugs.config import Config
from hexbugs.services import hooks

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
