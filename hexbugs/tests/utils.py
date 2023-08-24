def add_db_defaults(conn):
    c = conn.get_cursor()
    c.execute("INSERT INTO players (name) VALUES ('Weasel'), ('Bravd')")

    c.execute("SELECT id FROM players WHERE name = 'Weasel'")
    p1_id = c.fetchone()[0]

    c.execute("SELECT id FROM players WHERE name = 'Bravd'")
    p2_id = c.fetchone()[0]

    c.execute("INSERT INTO games DEFAULT VALUES")

    c.execute("SELECT id FROM games")
    game_id = c.fetchone()[0]

    c.execute(
        f"INSERT INTO game_players (game_id, player_id) VALUES ({game_id}, {p1_id}), ({game_id}, {p2_id})"
    )

    print("Weasel and Bravd join the game")

    return [game_id, p1_id, p2_id]
