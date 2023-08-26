from hexbugs.tests.test_triggers import test_change_players_trigger
from hexbugs.tests.test_rehydration import test_rehydration
from hexbugs.tests.test_bug_adds import test_bug_adds
from hexbugs.tests.test_message_handlers import TestGameManager
import unittest
import time


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestGameManager))
    return suite


if __name__ == '__main__':
    start_time = time.time()
    print("..")

    try:
        test_bug_adds()
        test_change_players_trigger()
        test_rehydration()
    except Exception as e:
        print(f"Tests failed with exception: {e}")
    else:
        time_taken = time.time() - start_time
        print(f"Ran 3 SQL tests in {time_taken:.3f}s")

    print("----------------------------------------------------------------------")


    runner = unittest.TextTestRunner()
    runner.run(suite())
