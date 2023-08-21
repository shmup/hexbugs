run:
    @env/bin/python mind/__init__.py

setup:
    @echo "Setting up the database"
    @sqlite3 hexbugs.db < sql/schema.sql

test:
    @just clean
    @just setup
    @env/bin/python tests/check_triggers.py
    @sqlite-utils hexbugs.db "select * from game_view" --table

clean:
    @echo "Removing hexbugs.db"
    @rm -f hexbugs.db
