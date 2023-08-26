from hexbugs.mind.models import Game, Player, Transaction, Bug
from hexbugs.mind.database import Session


class GameManager:

    def __init__(self):
        self.games = {}

    async def handle_message(self, message):
        if message['action'] == 'join':
            self.join_game(message)
        elif message['action'] == 'move':
            self.move_piece(message)

    def join_game(self, message):
        game_id = message['game_id']
        player_id = message['player_id']

        with Session() as session:
            game = session.query(Game).get(game_id)
            player = session.query(Player).get(player_id)

            if not game or not player:
                return

            game.players.append(player)
            session.commit()

            self.games[game_id] = game

    def move_piece(self, message):
        game_id = message['game_id']
        player_id = message['player_id']
        bug_id = message['bug_id']
        new_position = message['new_position']

        with Session() as session:
            game = session.query(Game).get(game_id)
            player = session.query(Player).get(player_id)
            bug = session.query(Bug).get(bug_id)

            if not game or not player or not bug:
                return

            transaction = Transaction(
                game_id=game_id,
                player_id=player_id,
                transaction_type_id=3,
                action=f'{{"bug_id": {bug.id}, "x": {new_position[0]}, "y": {new_position[1]}}}'
            )
            session.add(transaction)
            session.commit()
