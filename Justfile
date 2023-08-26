export PYTHONPATH:="."

run:
    @env/bin/python mind.py

setup: clean
    @echo "Setting up the database"
    @sqlite3 hexbugs/hexbugs.db < hexbugs/sql/schema.sql

history:
    @sqlite-utils hexbugs/hexbugs.db "SELECT * FROM game_history WHERE game_id = 1;" --table


peek:
    @sqlite-utils hexbugs/hexbugs.db "select * from game_view" --table

test: clean
    @env/bin/python hexbugs/tests/__init__.py

sync-to-dungeon:
    @rsync -avzp . dungeon.red:src/games/hexbugs/ \
      --exclude='__pycache__' \
      --exclude='.git' \
      --exclude='env'

run-seed-script: clean
    @env/bin/python hexbugs/seed.py

seed-db: run-seed-script
    @echo "Database seeded successfully!"

clean:
    @echo "Removing hexbugs.db"
    @rm -f hexbugs/hexbugs.db
