# hexbugs - a hive clone for 2 friends to play online

Solo project that doesn't have to be "enterprise scale" by any means..

## TODO
[x] - sqlite schema for game transactions
[ ] - backend data structures (node or python), for the api
[ ] - backend routing to start, progress, and end a game
[ ] - develop game state validators
[ ] - wire in database to backend
[ ] - slew of httpies to "play" a game (tests, sorta)
[ ] - develop websocket messages and callers
[ ] - render a hive with rot.js
[ ] - wire user events to websocket callers
[ ] - polish

## Frontend built out with

    https://ondras.github.io/rot.js/manual/#hex/about
    https://ondras.github.io/rot.js/manual/#hex/indexing

    Websockets talking to the Mind.

    In a perfect information game, nothing needs to be hidden.

    Enforce 4th move Queen requirement.
    Validate move legality.

    On load, hydrate a /gameId session if existing game.

    Features: chat, timer, sound effects

### Screens

1. main page just talks about hive and has a box to start a game which will either go to:
    #foo or /foo, not sure yet?
2. game page will have center column be the hive board
    2a. pieces to play will be beneath it, stacked and obvious how many in a stack
    2b. rules may even be visible in a collapsible column
    2c. chatbox eventually
3. hive board
    * show a green  line when mousing or holding mouse/finger down over
      a piece, making the possibilities obvious? if this is for a beetle,
      i guess the tops of tiles would have a green hue?
    * tile has a red hue when being held over an illegal move.
    * optional toggle to show # on tiles in order of last played/moved?
    * maybe always make last moved always have some indicator

## Mind built with python or javascript

Will start a game when someone makes a request, the ID being the #hash perhaps

Parse command:

    Command that concedes
    Command that adds a bug
    Command that moves a bug
    Command that chats

Validate command:

    Is a valid player
    Player turn
    Reject `turn>=4 && queen.sleeping`
    Reject illegal moves

## Storage

sqlite and localdb will be used.

sqlite will keep every command transaction, excluding chat.

localdb will remember any options? idk yet.


## Schema
```sql
CREATE TABLE players (
    id INTEGER PRIMARY KEY,
    name TEXT
);

/**
    The `state` field could be a JSON or similar string that represents the
    current state of the game. The `current_turn` field could be used to track
    who's turn it is (by player id).

    Ultimately, state is how you can re-render the page from nothing.
*/
CREATE TABLE games (
    id INTEGER PRIMARY KEY,
    player1_id INTEGER,
    player2_id INTEGER,
    current_turn INTEGER,
    state TEXT,
    FOREIGN KEY(player1_id) REFERENCES players(id),
    FOREIGN KEY(player2_id) REFERENCES players(id)
);

/**
    The `action` field could be a JSON or similar string that describes the
    action taken.
*/
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY,
    game_id INTEGER,
    player_id INTEGER,
    action TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(game_id) REFERENCES games(id),
    FOREIGN KEY(player_id) REFERENCES players(id)
);
```

## Rules
1. Initial Placement Rule: The first piece played by each player must be placed
   in the center of the playing area.

2. Touching Rule: Each new piece placed must be touching at least one of its
   player's own pieces, and no opponent's pieces.

3. Unity Rule: No move can be made that would cause any part of the hive to be
   disconnected.

4. Sliding Rule: A piece may be moved to any spot it can slide to without any
   other pieces being lifted or moved.

5. Freedom of Movement Rule: A piece has the freedom to move if it is not
   surrounded on four specific sides. In a hex grid, a piece can move unless it
   is touched by other pieces at four specific spots: n, n+1, n+3, n+4 (where
   n is the starting side and sides are numbered from 0 to 5 in a clockwise or
   counterclockwise direction). If these specific spots are blocked, the piece
   is stuck, unless it has the ability to jump or climb out, like the
   grasshopper or the beetle.

6. One Hive Rule: At all times, the hive must be one connected group of pieces,
   each touching another flat side to flat side.

7. No Recapture Rule: A piece, once moved, cannot be moved back to its original
   location on the player's next turn.

8. Queen Bee Rule: The queen bee must be placed by the fourth turn.

9. Beetle Rule: The beetle moves one space like the queen, but it can also
   climb on top of another piece and move over pieces.

10. Grasshopper Rule: The grasshopper jumps in a straight line over one or more
    pieces.

11. Spider Rule: The spider must move exactly three spaces, in one direction, per turn.

12. Ant Rule: The ant can move to any spot it can slide to.

13. Game End Rule: The game ends when a queen bee is surrounded on all six
    sides by pieces of any color, with that player losing the game.


## Theme

1. Beetle -> Scarab
    - They can climb over other bugs and move in any direction.

2. Spider -> Tarantula
    - They must move exactly three spaces around the hive.

3. Grasshopper -> Cricket
    - They can jump over other bugs to an unoccupied space on the other side.

4. Soldier Ant -> Wasp
    - They can move to any unoccupied space around the hive.

5. Queen Bee -> Monarch Butterfly
    - They can move to any adjacent space.

6. Mosquito -> Tick
    - They can mimic the movement of any bug they touch.

7. Ladybug -> Firefly
    - They can move three spaces; two on top of the hive and one down.

8. Pillbug -> Roly Poly
    - They can move one space or move an adjacent piece to another empty space adjacent to itself.
