from colorama import Fore, Style
from hexbugs.mind.models import Transaction
from hexbugs.mind.database import Session
from hexbugs.tests.utils import add_db_defaults


def test_bug_adds():
    with Session() as session:
        print("test_bug_adds()")

        try:
            [game_id, _, __] = add_db_defaults()

            t1 = Transaction(game_id=1, player_id=1, transaction_type_id=3, action='{"bug_id": 2, "x": 0, "y": 0}')
            t2 = Transaction(game_id=1, player_id=2, transaction_type_id=3, action='{"bug_id": 16, "x": 1, "y": 0}')
            session.add(t1)
            session.add(t2)

            transactions = session.query(Transaction).filter(
                Transaction.game_id == game_id).all()
            assert transactions, "Weasel and Bravd should have both added a bug"

            print(f'{Fore.LIGHTGREEN_EX}Weasel and Bravd both added a bug{Style.RESET_ALL}')
            print("---------------")

        except Exception as e:
            session.rollback()
            raise e
