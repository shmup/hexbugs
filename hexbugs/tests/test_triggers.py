from colorama import Fore, Style
from hexbugs.mind.models import Game
from hexbugs.mind.database import Session
from hexbugs.tests.utils import add_db_defaults

def test_change_players_trigger():
    session = Session()
    with session.begin_nested():
        print("test_change.players_trigger()")

        [game_id, weasel_id, bravd_id] = add_db_defaults()

        game = session.query(Game).filter(Game.id == game_id).one()
        game.current_turn = weasel_id

        current_turn = session.query(
            Game.current_turn).filter(Game.id == game_id).scalar()
        assert current_turn == weasel_id, "Current turn should be Weasel after Weasel's move"

        print("Weasel took a turn")

        game.current_turn = bravd_id

        current_turn = session.query(
            Game.current_turn).filter(Game.id == game_id).scalar()
        assert current_turn == bravd_id, "Current turn should be Bravd after Bravd's move"

        print("Bravd took a turn")
        print(f'{Fore.LIGHTGREEN_EX}Current turn correctly set after both took a turn{Style.RESET_ALL}')
        print("---------------")

    session.close()
