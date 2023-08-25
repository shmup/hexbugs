from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from hexbugs.config import Config
from hexbugs.mind.models import Base
from hexbugs.mind.models import Bug, TransactionType

engine = create_engine(f"sqlite:///{Config.DB_PATH}")
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

bugs = [
    'Queen', 'Beetle', 'Spider', 'Grasshopper', 'Ant', 'Ladybug', 'Mosquito',
    'Pillbug'
]
for bug in bugs:
    new_bug = Bug(name=bug)
    session.add(new_bug)

transaction_types = ['ready', 'forfeit', 'add', 'move']
for transaction_type in transaction_types:
    new_transaction_type = TransactionType(type=transaction_type)
    session.add(new_transaction_type)

session.commit()
