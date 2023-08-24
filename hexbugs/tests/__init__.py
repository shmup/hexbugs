from hexbugs.tests.test_triggers import test_change_players_trigger
from hexbugs.tests.test_rehydration import test_rehydration
from hexbugs.tests.test_bug_adds import test_bug_adds
from hexbugs.mind.db import DBHandler

db_handler = DBHandler('hexbugs.db')

if __name__ == '__main__':
    test_change_players_trigger(db_handler)
    test_rehydration(db_handler)
    test_bug_adds(db_handler)
