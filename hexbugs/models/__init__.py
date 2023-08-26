from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from hexbugs.database import Base


class Bug(Base):
    __tablename__ = 'bugs'
    id = Column(Integer, primary_key=True)
    name = Column(String)


# In this schema, an `Action` represents either an 'add' or 'move' operation, and
# is associated with a `Bug` and a position. A `Transaction` represents the
# action of a `Player` in a `Game`, and is associated with an `Action`. The
# `ActionType` table allows you to add new types of actions in the future without
# changing your schema.


class Player(Base):
    __tablename__ = 'players'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    transactions = relationship('Transaction', back_populates='player')
    game_players = relationship('GamePlayer', back_populates='player')


class Game(Base):
    __tablename__ = 'games'
    id = Column(Integer, primary_key=True)
    current_turn = Column(Integer, ForeignKey('players.id'))
    game_over = Column(Integer, default=0)
    transactions = relationship('Transaction', back_populates='game')
    game_players = relationship('GamePlayer', back_populates='game')


class GamePlayer(Base):
    __tablename__ = 'game_players'
    game_id = Column(Integer, ForeignKey('games.id'), primary_key=True)
    player_id = Column(Integer, ForeignKey('players.id'), primary_key=True)
    player = relationship('Player', back_populates='game_players')
    game = relationship('Game', back_populates='game_players')

    def __init__(self, game_id, player_id):
        self.game_id = game_id
        self.player_id = player_id


class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey('games.id'))
    player_id = Column(Integer, ForeignKey('players.id'))
    action_id = Column(Integer, ForeignKey('actions.id'))
    timestamp = Column(DateTime, default=func.now())
    player = relationship('Player', back_populates='transactions')
    game = relationship('Game', back_populates='transactions')
    action = relationship('Action')

    def __init__(self, game_id, player_id, action_id):
        self.game_id = game_id
        self.player_id = player_id
        self.action_id = action_id

class ActionType(Base):
    __tablename__ = 'action_types'
    id = Column(Integer, primary_key=True)
    type = Column(String)


class Action(Base):
    __tablename__ = 'actions'
    id = Column(Integer, primary_key=True)
    action_type_id = Column(Integer, ForeignKey('action_types.id'))
    bug_id = Column(Integer, ForeignKey('bugs.id'))
    x = Column(Integer)
    y = Column(Integer)
    z = Column(Integer)


class MoveBug(Base):
    __tablename__ = 'add_bugs'
    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey('games.id'))
    player_id = Column(Integer, ForeignKey('players.id'))
    bug_id = Column(Integer, ForeignKey('bugs.id'))
    x = Column(Integer)
    y = Column(Integer)
    z = Column(Integer)
    timestamp = Column(DateTime, default=func.now())
