from hexbugs.mind.models import Game
from hexbugs.mind.database import Session
from hexbugs.tests.utils import add_db_defaults


def test_change_players_trigger():
    session = Session()
    with session.begin_nested():
        [game_id, weasel_id, bravd_id] = add_db_defaults()

        game = session.query(Game).filter(Game.id == game_id).one()
        game.current_turn = weasel_id

        current_turn = session.query(
            Game.current_turn).filter(Game.id == game_id).scalar()
        assert current_turn == weasel_id, "Current turn should be Weasel after Weasel's move"

        game.current_turn = bravd_id

        current_turn = session.query(
            Game.current_turn).filter(Game.id == game_id).scalar()
        assert current_turn == bravd_id, "Current turn should be Bravd after Bravd's move"

    session.close()
