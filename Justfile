run:
        @env/bin/python mind/__init__.py

setup:
	@echo "Setting up the database..."
	@sqlite3 hexbugs.db < schema.sql

browse:

clean:
        rm hexbugs.db
