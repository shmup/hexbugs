from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Bug(Base):
    __tablename__ = 'bugs'
    id = Column(Integer, primary_key=True)
    name = Column(String)


class Game(Base):
    __tablename__ = 'games'
    id = Column(Integer, primary_key=True)
    current_turn = Column(Integer, ForeignKey('players.id'))
    game_over = Column(Integer, default=0)
    state = Column(String)
    transactions = relationship("Transaction", backref="game")


class Player(Base):
    __tablename__ = 'players'
    id = Column(Integer, primary_key=True)
    name = Column(String)


class GamePlayer(Base):
    __tablename__ = 'game_players'
    game_id = Column(Integer, ForeignKey('games.id'), primary_key=True)
    player_id = Column(Integer, ForeignKey('players.id'), primary_key=True)


class TransactionType(Base):
    __tablename__ = 'transaction_types'
    id = Column(Integer, primary_key=True)
    type = Column(String)


class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey('games.id'))
    player_id = Column(Integer, ForeignKey('players.id'))
    transaction_type_id = Column(Integer, ForeignKey('transaction_types.id'))
    action = Column(String)
    timestamp = Column(DateTime, default=func.now())

    def __init__(self, game_id, player_id, transaction_type_id, action):
        self.game_id = game_id
        self.player_id = player_id
        self.transaction_type_id = transaction_type_id
        self.action = action
