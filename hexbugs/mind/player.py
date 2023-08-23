from hexbugs.mind.db import DBHandler
import json


def add_player(name):
    with DBHandler('hexbugs.db') as cursor:
        cursor.execute("INSERT INTO players (name) VALUES (?)", (name,))


def add_bug(game_id, player_id, bug_id, x, y):
    with DBHandler('hexbugs.db') as cursor:
        action = json.dumps({
            "type": "add",
            "bug_id": bug_id,
            "x": x,
            "y": y
        })
        cursor.execute(
            "INSERT INTO transactions (game_id, player_id, action) VALUES (?, ?, ?)",
            (game_id, player_id, action))


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
