from colorama import Fore, Style
from hexbugs.mind import player
from hexbugs.tests.utils import add_db_defaults
import sqlite3


def test_rehydration():
    conn = sqlite3.connect('hexbugs.db')
    c = conn.cursor()
    c.execute('BEGIN')

    try:
        [game_id, weasel_id, bravd_id] = add_db_defaults(c)

        conn.commit()

        data = player.rehydrate_game(game_id)
        assert data == ((1, 1, 0, None), [(1, 'Weasel'), (2, 'Bravd')], [])


        print(Fore.LIGHTGREEN_EX + "Rehydration matches as expected!" + Style.RESET_ALL)
        print("---------------")

        c.execute(f"DELETE FROM game_players WHERE game_id = {game_id}")
        c.execute(f"DELETE FROM games WHERE id = {game_id}")
        c.execute(f"DELETE FROM players WHERE id IN ({weasel_id}, {bravd_id})")

        conn.commit()

    except Exception as e:
        print(f'Error: {e}')

    finally:
        conn.close()


if __name__ == '__main__':
    test_rehydration()
