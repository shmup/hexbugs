from enum import Enum, auto

class Triggers(Enum):
    ENFORCE_CURRENT_TURN_ON_INSERT = auto()
    ENFORCE_CURRENT_TURN_ON_UPDATE = auto()


player_not_in_game_template = """
  CREATE TRIGGER IF NOT EXISTS {name}
  BEFORE {action} ON games
  FOR EACH ROW
  BEGIN
      SELECT CASE
          WHEN (SELECT COUNT(*) FROM game_players WHERE game_id = NEW.id AND player_id = NEW.current_turn) = 0 THEN
          RAISE(ABORT, 'Current turn must be one of the players')
      END;
  END;
  """


