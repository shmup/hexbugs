export PYTHONPATH:="."

run:
    @just setup
    @env/bin/python hexbugs/__init__.py

setup: clean
    @echo "Setting up the database"
    @sqlite3 hexbugs.db < sql/schema.sql

peek:
    @sqlite-utils hexbugs.db "select * from game_view" --table

test: clean setup
    @env/bin/python hexbugs/tests/__init__.py

sync-to-dungeon:
    @rsync -avzp . dungeon.red:src/games/hexbugs/ \
      --exclude='__pycache__' \
      --exclude='.git' \
      --exclude='env'

clean:
    @echo "Removing hexbugs.db"
    @rm -f hexbugs.db
