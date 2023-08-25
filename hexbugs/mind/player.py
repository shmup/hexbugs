import json

from hexbugs.mind.models import Transaction, GamePlayer, Game
from sqlalchemy.exc import NoResultFound
import json


def add_bug(session, game_id, player_id, bug_id, x, y):
    action = json.dumps({"bug_id": bug_id, "x": x, "y": y})
    transaction_type = 3
    new_transaction = Transaction(
        game_id=game_id,
        player_id=player_id,
        transaction_type_id=transaction_type,
        action=action)
    session.add(new_transaction)
    session.commit()


def rehydrate_game(session, game_id):
    try:
        game = session.query(Game).filter(Game.id == game_id).one()
        players = session.query(GamePlayer).filter(
            GamePlayer.game_id == game_id).all()
        transactions = session.query(Transaction).filter(
            Transaction.game_id == game_id).order_by(
                Transaction.timestamp.desc()).all()
        return game, players, transactions

    except NoResultFound:
        return None
