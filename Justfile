run:
    @env/bin/python mind/__init__.py

setup:
    @echo "Setting up the database"
    @sqlite3 hexbugs.db < sql/schema.sql

test:
    @just clean
    @just setup
    @sqlite3 hexbugs.db < sql/test_automated_current_turn_trigger.sql

clean:
    @echo "Removing hexbugs.db"
    @rm -f hexbugs.db
