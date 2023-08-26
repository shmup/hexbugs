from hexbugs.models import Action, ActionType, Bug, Game, Player, Transaction
from hexbugs.database import Session


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

            # Get the 'move' action_type_id
            action_type = session.query(ActionType).filter_by(
                type='move').first()
            if not action_type:
                return

            # Create a new Action
            action = Action(
                action_type_id=action_type.id,
                bug_id=bug_id,
                x=new_position['x'],
                y=new_position['y'],
                z=new_position['z'])
            session.add(action)
            session.commit()

            # Create a new Transaction
            transaction = Transaction(
                game_id=game_id, player_id=player_id, action_id=action.id)
            session.add(transaction)
            session.commit()
