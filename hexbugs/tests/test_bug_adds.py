from hexbugs.models import Action, Transaction
from hexbugs.database import Session
from hexbugs.tests.utils import add_db_defaults


def test_bug_adds():
    with Session() as session:
        try:
            [game_id, weasel_id, bravd_id] = add_db_defaults()

            a1 = Action(action_type_id=3, bug_id=2, x=0, y=0)
            a2 = Action(action_type_id=3, bug_id=16, x=1, y=0)
            session.add(a1)
            session.add(a2)
            session.commit()

            t1 = Transaction(
                game_id=game_id, player_id=weasel_id, action_id=a1.id)
            t2 = Transaction(
                game_id=game_id, player_id=bravd_id, action_id=a2.id)
            session.add(t1)
            session.add(t2)

            transactions = session.query(Transaction).filter(
                Transaction.game_id == game_id).all()
            assert transactions, "Weasel and Bravd should have both added a bug"
        except Exception as e:
            session.rollback()
            raise e
