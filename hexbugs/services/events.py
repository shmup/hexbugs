from hexbugs.models import GamePlayer, Bug
from hexbugs.models import Game
from hexbugs.database import Session
from sqlalchemy import or_


def set_first_turn(_, connection, target):
    with Session() as session:
        game = session.query(Game).get(target.game_id)
        if not game:
            return
        players = connection.query(GamePlayer)\
            .filter(GamePlayer.game_id == target.game_id)\
            .order_by(GamePlayer.player_id).all()
        if len(players) == 2:
            game.current_turn = players[0].player_id



def update_turn_after_transaction(_, connection, target):
    if target.action.action_type.type in ('add', 'move'):
        game_player = connection.query(GamePlayer)\
            .filter(GamePlayer.game_id == target.game_id,
                    or_(GamePlayer.player_id != target.game.current_turn,
                        target.game.current_turn == None))\
            .order_by(GamePlayer.player_id)\
            .first()
        if game_player:
            target.game.current_turn = game_player.player_id

def verify_bug_id_before_transaction(_, connection, target):
    bug_exists = connection.query(Bug).filter(Bug.id == target.action.bug_id).first()
    if not bug_exists:
        raise Exception('Invalid bug_id')

