from sqlalchemy import event
from hexbugs.services.events import set_first_turn, verify_bug_id_before_transaction, update_turn_after_transaction
from hexbugs.models import GamePlayer, Transaction

event.listen(GamePlayer, 'after_insert', set_first_turn)
event.listen(Transaction, 'before_insert', verify_bug_id_before_transaction)
event.listen(Transaction, 'after_insert', update_turn_after_transaction)
