# Import your database models here

from models import Game, Player, Transaction

class GameManager:
    def __init__(self):
        self.games = {} # Store games by ID

    async def handle_message(self, message):
        if message['action'] == 'join':
            self.join_game(message)
        elif message['action'] == 'move':
            self.move_piece(message)
        # Add more elif clauses here to handle other message actions
    
    def join_game(self, message):
        game_id = message['game_id']
        player_id = message['player_id']
        # Fetch the game and player from the database
        game = Game.query.get(game_id)
        player = Player.query.get(player_id)
        
        if not game or not player:
            return # Handle this error appropriately
        
        # Add the player to the game
        game.players.append(player)
        db.session.commit() # Assuming db is your SQLAlchemy session

        self.games[game_id] = game # Add the game to our in-memory store

    def move_piece(self, message):
        game_id = message['game_id']
        player_id = message['player_id']
        bug_id = message['bug_id']
        new_position = message['new_position']

        # Fetch the game, player, and bug from the database
        game = Game.query.get(game_id)
        player = Player.query.get(player_id)
        bug = Bug.query.get(bug_id)

        if not game or not player or not bug:
            return # Handle this error appropriately

        # Validate the move here, then
        # Record the move in a new Transaction
        transaction = Transaction(game=game, player=player, type='move', action=f'{bug.name} to {new_position}')
        db.session.add(transaction)
        db.session.commit()
