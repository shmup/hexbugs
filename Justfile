setup:
	@echo "Setting up the database..."
	@sqlite3 hexbugs.db < schema.sql

clean:
        rm hexbugs.db
