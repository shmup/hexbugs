from db import DBHandler

def add_player(name):
  with DBHandler('hexbugs.db') as cursor:
    cursor.execute("INSERT INTO players (name) VALUES (?)", (name,))
