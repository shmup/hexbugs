from colorama import Fore, Style
from hexbugs.mind import player
from hexbugs.tests.utils import add_db_defaults


def test_rehydration(conn):
    c = conn.get_cursor()
    c.execute('BEGIN')
    print("test_rehydration()")

    try:
        [game_id, weasel_id, bravd_id] = add_db_defaults(conn)

        conn.commit()

        data = player.rehydrate_game(conn, game_id)
        assert data == ((1, 1, 0, None), [(1, 'Weasel'), (2, 'Bravd')], [])

        print(f'{Fore.LIGHTGREEN_EX}Rehydration matches as expected{Style.RESET_ALL}')
        print("---------------")

        c.execute(f"DELETE FROM game_players WHERE game_id = {game_id}")
        c.execute(f"DELETE FROM games WHERE id = {game_id}")
        c.execute(f"DELETE FROM players WHERE id IN ({weasel_id}, {bravd_id})")

        conn.commit()

    except Exception as e:
        print(f'{Fore.RED}Error: {e}{Style.RESET_ALL}')

    finally:
        conn.rollback()
