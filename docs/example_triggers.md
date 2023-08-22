```python
db_handler.create_trigger(
    Triggers.ENFORCE_CURRENT_TURN_ON_INSERT.name,
    player_not_in_game_template.format(
        name=Triggers.ENFORCE_CURRENT_TURN_ON_INSERT.name,
        action='INSERT'))
```
