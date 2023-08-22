```python
db_handler.create_trigger(
    Triggers.ENFORCE_CURRENT_TURN_ON_INSERT.name,
    player_not_in_game_template.format(
        name=Triggers.ENFORCE_CURRENT_TURN_ON_INSERT.name,
        action='INSERT'))
```

```python
# triggers.py

from enum import Enum, auto


class Triggers(Enum):
    ENFORCE_CURRENT_TURN_ON_INSERT = auto()
    ENFORCE_CURRENT_TURN_ON_UPDATE = auto()


player_not_in_game_template = """
  CREATE TRIGGER IF NOT EXISTS {name}
  AFTER {action} ON games
  FOR EACH ROW
  BEGIN
      SELECT CASE
          WHEN (SELECT COUNT(*) FROM game_players WHERE game_id = NEW.id AND player_id = NEW.current_turn) = 0 THEN
          RAISE(ABORT, 'Current turn must be one of the players')
      END;
  END;
  """
```
