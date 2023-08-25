"""
# Responsible for the game state of hexbugs.

So the server starts up and listens. It's basically doing nothing.

## Lobby joining
> A player signals they join a lobby.
! The Mind creates a new game in the database for the player_id and lobby_name.
< The initial gamestate is sent to player 1.

They can just move pieces around right now, until another player joins.
    * Make this very obvious, if not even only visible to that player and not
      communicated to the Mind

> A player signals they joins the same lobby.
! The Mind updates the game record.
< The initial gamestate is sent to player 2.
< The updated gamestate is sent to player 1.

## Choosing who goes first
> Player 1 rolls a d20
! The Mind rolls a dice and updates the game record.
< The updated gamestate is sent to both players.
> Player 2 rolls a d20
! The Mind rolls a dice and updates the game record.
! The Mind sets the current_turn to winner.
< The updated gamestate is sent to both players.
    * A reroll may have to happen.

First to move has color choice?

## Adding first bug to hive
> A player signals they add `bugId` to x,y
! The Mind validates the move
    * Though, the UI will also be _trying_ to validate
! The Mind updates the game record.
< The updated gamestate is sent to both players.


...TODO
"""

pieces = {
  "pieces": [
    {
      "type": "queen_bee"
    },
    {
      "type": "spider"
    },
    {
      "type": "ant"
    },
    {
      "type": "beetle"
    },
    {
      "type": "grasshopper"
    },
  ]
}
"""
This should be able to inform a players screen a number of things:

State of pieces, where on board.

Whose turn it is.

If the game is over, and who won (or a draw).

What the last move of the game was (some signaling).
"""

# Initial
game_state = {
  "id": 0,
  "lobby": "bugsnax",
  "gameover": 0,
  "current_turn": 0,  # player id
  "players": [],  # player ids
  "status": "ongoing",  # or "completed"
  "winner": None # otherwise, a player id
}

# Update
mock_game_update = {
  "id": 0,
  "player": 1,
  "play": {
    "player": 1,
    "action": "move",
    "bug_id": 5,
    "coords": [1, 1, 0]
  },  # a add or movement
}

# Mock Rehydration (full game_state, say, a hard refresh or something)
mock_rehydrated_game_state = {
  "id": 0,
  "lobby": "bugsnax",
  "current_turn": 0,  # player id
  "gameover": 0,
  "players": [],  # player ids
  "plays": [
    {
      "player": 1,
      "action": "add",
      "bug_id": 5,
      "coords": [1, 1]
    },
    {
      "player": 2,
      "action": "add",
      "bug_id": 12,
      "coords": [1, 2]
    },
    {
      "player": 1,
      "action": "move",
      "bug_id": 5,
      "coords": [1, 4]
    },
    {
      "player": 2,
      "action": "move",
      "bug_id": 12,
      "coords": [3, 2]
    },
  ]
}
