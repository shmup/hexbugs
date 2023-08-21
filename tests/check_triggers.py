import sqlite3
import json


def test_triggers():
    conn = sqlite3.connect('hexbugs.db')
    c = conn.cursor()

    c.execute('BEGIN')
    try:
        c.execute("INSERT INTO players (name) VALUES ('Weasel'), ('Bravd')")

        c.execute("SELECT id FROM players WHERE name = 'Weasel'")
        weasel_id = c.fetchone()[0]

        c.execute("SELECT id FROM players WHERE name = 'Bravd'")
        bravd_id = c.fetchone()[0]

        c.execute("INSERT INTO games DEFAULT VALUES")

        c.execute("SELECT id FROM games")
        game_id = c.fetchone()[0]

        c.execute(
            f"INSERT INTO game_players (game_id, player_id) VALUES ({game_id}, {weasel_id}), ({game_id}, {bravd_id})"
        )

        c.execute(
            f"INSERT INTO transactions (game_id, player_id, action) VALUES ({game_id}, {weasel_id}, ?)",
            (json.dumps({
                "type": "add",
                "bug": 1
            }),))

        c.execute(f'SELECT current_turn FROM games WHERE id = {game_id}')
        assert c.fetchone(
        )[0] == bravd_id, "Current turn should be Bravd after Weasel's move"

        c.execute(
            f"INSERT INTO transactions (game_id, player_id, action) VALUES ({game_id}, {bravd_id}, ?)",
            (json.dumps({
                "type": "add",
                "bug": 2
            }),))

        c.execute(f'SELECT current_turn FROM games WHERE id = {game_id}')
        assert c.fetchone(
        )[0] == weasel_id, "Current turn should be Weasel after Bravd's move"

        conn.commit()

    except Exception as e:
        print(f'Error: {e}')
        conn.rollback()

    finally:
        conn.close()


if __name__ == '__main__':
    test_triggers()
