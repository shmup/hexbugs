import os

class Config:
    DEBUG = False
    HOST = 'localhost'
    PORT = 8765
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DB_PATH = os.path.join(BASE_DIR, 'hexbugs.db')
    SQL_PATH = os.path.join(BASE_DIR, 'sql/schema.sql')
