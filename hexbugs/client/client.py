import json
from websockets.sync.client import connect
from hexbugs.config import Config


class GameClient:

    def __init__(self, uri):
        self.uri = uri

    def connect(self):
        self.connection = connect(self.uri)

    def send_message(self, message):
        with self.connection as websocket:
            websocket.send(json.dumps(message))

    def receive_message(self):
        with self.connection as websocket:
            response = websocket.recv()
            return json.loads(response)


def main():
    client = GameClient(f"ws://{Config.HOST}:{Config.PORT}")

    client.connect()
    print('Connected')

    join_message = {'action': 'join'}
    client.send_message(join_message)
    print('Join message sent')

    response = client.receive_message()
    print('Received response:', response)


main()
