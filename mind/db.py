import sqlite3
from triggers import Triggers, player_not_in_game_template

def initialize_db(db_name):
    db_handler = DBHandler(db_name)
    with db_handler as cursor:
        with open('schema.sql', 'r') as f:
            cursor.executescript(f.read())

            db_handler.create_trigger(
                Triggers.ENFORCE_CURRENT_TURN_ON_INSERT.name,
                player_not_in_game_template.format(
                    name=Triggers.ENFORCE_CURRENT_TURN_ON_INSERT.name,
                    action='INSERT'))

            db_handler.create_trigger(
                Triggers.ENFORCE_CURRENT_TURN_ON_UPDATE.name,
                player_not_in_game_template.format(
                    name=Triggers.ENFORCE_CURRENT_TURN_ON_UPDATE.name,
                    action='UPDATE'))


class DBHandler:

    def __init__(self, db_name):
        self.db_name = db_name

    def trigger_exists(self, trigger_name):
        self.cursor.execute(
            f"SELECT name FROM sqlite_master WHERE type='trigger' AND name='{trigger_name}'"
        )
        return self.cursor.fetchone() is not None

    def create_trigger(self, trigger_name, sql_string):
        if not self.trigger_exists(trigger_name):
            self.cursor.execute(sql_string)

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        _ = exc_type, exc_val, exc_tb  # are you happy pyright
        self.conn.commit()
        self.conn.close()