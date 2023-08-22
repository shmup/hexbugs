import sqlite3
from hexbugs.mind import player


def test_rehydration():
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

        print("Weasel and Bravd join the game")

        conn.commit()

        data = player.rehydrate_game(game_id)

        print(data)

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
