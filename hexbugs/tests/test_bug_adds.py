from colorama import Fore, Style
from hexbugs.mind import player
from hexbugs.tests.utils import add_db_defaults
import sqlite3


def test_bug_adds():
    conn = sqlite3.connect('hexbugs.db')
    c = conn.cursor()
    c.execute('BEGIN')

    try:
        [game_id, weasel_id, bravd_id] = add_db_defaults(c)
        conn.commit()
        player.add_bug(game_id, weasel_id, 2, 0, 0)
        player.add_bug(game_id, bravd_id, 16, 1, 0)

        [_, __, transactions] = player.rehydrate_game(game_id)
        [t1, t2] = transactions
        t1_expected = (1, 1, 1, '{"type": "add", "bug_id": 2, "x": 0, "y": 0}')
        t2_expected = (2, 1, 2, '{"type": "add", "bug_id": 16, "x": 1, "y": 0}')
        assert t1[:-1] == t1_expected
        assert t2[:-1] == t2_expected

        print(f'{Fore.LIGHTGREEN_EX}Weasel and Bravd both added a bug{Style.RESET_ALL}')
        print("---------------")

    except Exception as e:
        print(f'{Fore.RED}Error: {e}{Style.RESET_ALL}')

    finally:
        conn.rollback()
        conn.close()


if __name__ == '__main__':
    test_bug_adds()
