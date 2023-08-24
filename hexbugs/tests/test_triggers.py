from colorama import Fore, Style
from hexbugs.mind import player
from hexbugs.tests.utils import add_db_defaults


def test_change_players_trigger(conn):
    c = conn.get_cursor()
    c.execute('BEGIN')
    print("test_change.players_trigger()")

    try:
        [game_id, weasel_id, bravd_id] = add_db_defaults(conn)

        player.add_bug(conn, game_id, weasel_id, 1, 1, 0)

        c.execute(f'SELECT current_turn FROM games WHERE id = {game_id}')
        assert c.fetchone(
        )[0] == bravd_id, "Current turn should be Bravd after Weasel's move"

        print("Weasel took a turn")

        player.add_bug(conn, game_id, bravd_id, 2, 0, 0)

        c.execute(f'SELECT current_turn FROM games WHERE id = {game_id}')
        assert c.fetchone(
        )[0] == weasel_id, "Current turn should be Weasel after Bravd's move"

        print("Bravd took a turn")
        print(
            f'{Fore.LIGHTGREEN_EX}Current turn correctly set after both took a turn{Style.RESET_ALL}'
        )
        print("---------------")
    except Exception as e:
        print(f'{Fore.RED}Error: {e}{Style.RESET_ALL}')

    finally:
        conn.rollback()
