export PYTHONPATH:="."

run:
    @just setup
    @env/bin/python hexbugs/__init__.py

setup: clean
    @echo "Setting up the database"
    @sqlite3 hexbugs.db < sql/schema.sql

peek:
    @sqlite-utils hexbugs.db "select * from game_view" --table

test:
    @just clean
    @just setup
    @env/bin/python tests/check_triggers.py

sync-to-dungeon:
    @rsync -avzp --exclude='.git' --exclude='env' . dungeon.red:src/games/hexbugs/

clean:
    @echo "Removing hexbugs.db"
    @rm -f hexbugs.db
