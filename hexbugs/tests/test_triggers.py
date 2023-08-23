import sqlite3
import json
from colorama import Fore, Style
from hexbugs.tests.utils import add_db_defaults


def test_change_players_trigger():
    conn = sqlite3.connect('hexbugs.db')
    c = conn.cursor()
    c.execute('BEGIN')

    try:
        [game_id, weasel_id, bravd_id] = add_db_defaults(c)

        c.execute(
            f"INSERT INTO transactions (game_id, player_id, action) VALUES ({game_id}, {weasel_id}, ?)",
            (json.dumps({
                "type": "add",
                "bug_id": 1
            }),))

        c.execute(f'SELECT current_turn FROM games WHERE id = {game_id}')
        assert c.fetchone(
        )[0] == bravd_id, "Current turn should be Bravd after Weasel's move"

        print("Weasel took a turn")

        c.execute(
            f"INSERT INTO transactions (game_id, player_id, action) VALUES ({game_id}, {bravd_id}, ?)",
            (json.dumps({
                "type": "add",
                "bug_id": 2
            }),))

        c.execute(f'SELECT current_turn FROM games WHERE id = {game_id}')
        assert c.fetchone(
        )[0] == weasel_id, "Current turn should be Weasel after Bravd's move"

        print("Bravd took a turn")
        print(Fore.LIGHTGREEN_EX + "Current turn correctly set after both took a turn" + Style.RESET_ALL)
        print("---------------")
    except Exception as e:
        print(f'Error: {e}')

    finally:
        conn.rollback()
        conn.close()


if __name__ == '__main__':
    test_change_players_trigger()
