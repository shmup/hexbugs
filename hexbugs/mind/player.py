from db import DBHandler


def add_player(name):
    with DBHandler('hexbugs.db') as cursor:
        cursor.execute("INSERT INTO players (name) VALUES (?)", (name,))


def rehydrate_game(game_id):
    with DBHandler('hexbugs.db') as cursor:
        # Get the game
        cursor.execute("SELECT * FROM games WHERE id = ?", (game_id,))
        game = cursor.fetchone()

        # Get the players
        cursor.execute(
            """
            SELECT players.*
            FROM players
            JOIN game_players ON players.id = game_players.player_id
            WHERE game_players.game_id = ?
        """, (game_id,))
        players = cursor.fetchall()

        # Get the transactions
        cursor.execute(
            """
            SELECT *
            FROM transactions
            WHERE game_id = ?
            ORDER BY timestamp DESC
        """, (game_id,))
        transactions = cursor.fetchall()

    return game, players, transactions
