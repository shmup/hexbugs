from hexbugs.mind.db import DBHandler
import json


def add_player(name):
    with DBHandler('hexbugs.db') as cursor:
        cursor.execute("INSERT INTO players (name) VALUES (?)", (name,))


def add_bug(conn, game_id, player_id, bug_id, x, y):
    cursor = conn.get_cursor()
    action = json.dumps({"bug_id": bug_id, "x": x, "y": y})
    transaction_type = 3
    cursor.execute(
        "INSERT INTO transactions (game_id, player_id, transaction_type_id, action) VALUES (?, ?, ?, ?)",
        (game_id, player_id, transaction_type, action))


def rehydrate_game(conn, game_id):
    cursor = conn.get_cursor()
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
