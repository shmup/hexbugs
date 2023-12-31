# hexbugs - a hive clone for 2 friends to play online

## FIRST PASS TODO
[x] - sqlite schema for game transactions
[x] - websocket message handlers in python
[x] - wire in sqlite database to backend

## SECOND PASS TODO
[x] - normalize the db
    - add a transactions and transaction type table
        * types are ready, concede, add, move (as in adding and moving an insect in a game_id)
[x] - sql queries / db method
        [x] 1. complete rehydration query, `game`, `game_players` and every
               transaction.
        [x] 2. move and add bugs
[x] - gamestate data structures used by our websocket api
        [x] 1. add a data structure for initial game state
        [x] 2. add a data structure for a game update
        [x] 3. add a complete data structure for rehydration w/ history
[x] - refactor sql into sqlalchemy
[x] - develop some sort of GameManager class that the websocket messages get
      passed to an instance of or something?

      right now mind/__init__.py has a main function:
       async def main():
           async with serve(handle_message, "localhost", 8765):
               print("The Mind awakes...")
               await asyncio.Future()

      And handle_message is a basic stubbed out async function that iterates
      over messages in the websocket
[ ] - develop game state validation used by websocket api
    Hm, okay so..

    * A player tries to do some sorta thing
    * Everything the player Can do runs through an FSM
        1. is concede? concedes.
        2. is players turn?
        3. is add? is touching hive? is not touching enemy? is not seppuku?? add.
        4. is move? doesnt temporarily cause 2 hives? is valid to insect type? 
        5. queens surrounded?
[ ] - develop needed websocket messages for a game
        * the idea is that the UI can know the entire game state.
        * the game _can_ rehydrate if needed but the player will receive messages
          that update their frontend board, and pieces not yet added to hive
        * updates include joining game, movements, additions to hive,
          conceding, gameover
[ ] - develop quick hacky debug UI w/ buttons to simulate a game
[ ] - wire user events to websocket callers

## THIRD PASS TODO
[ ] - render a hive with rot.js
[ ] - develop the game UI

## FOURTH PASS TODO
[ ] - authentication
[ ] - polish

## Mind built with python

Will start a game when someone makes a request, the ID either a #hash or /slug.

It must have a "GameManager" which I haven't spec'd out yet, but seems like it'd be a gateway that
looks up if the slug is a valid game and if the player is in that game, or maybe you can spectate anyways

If it is the player_id or the lobby is open/waiting then update whatever state

I suppose all clients are blasting messages to this Mind though, and the mind is passing them to something I haven't developed yet. I'm lacking in the "class" department, though needn't necessarily be classes vs modules. Anyways..

Websockets server that handles a variety of messages.

1. player can join a game, keyed on lobby name
2. player can concede
3. player can add a bug to the hive
4. playe can move a bug on the hive
5. player can send a message/chat

It will also do some validation, such as:

1. is player taking an action in game
2. is it their turn
3. if turn 4, is queen played yet bc required to
4. move legality in general for the various types of insects

The database is basically a table of games and a table of transactions that
constitute actions in a game.

## Frontend built out with

    https://ondras.github.io/rot.js/manual/#hex/about
    https://ondras.github.io/rot.js/manual/#hex/indexing

    Websockets talking to the Mind.

    In a perfect information game, nothing needs to be hidden.

    Enforce 4th move Queen requirement.
    Validate move legality.

    On load, hydrate a /gameId session if existing game.

    Features: chat, timer, sound effects

## Storage

sqlite and localdb will be used.

sqlite will keep every command transaction.

localdb will remember any options? idk yet.

## Schema

Peek `sql/schema.sql`

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

8. Queen Bee: The Queen Bee can only move one space at a time, but it is the
   most important piece. If it gets surrounded by pieces, either your own or
   your opponent's, you lose the game.

9. Beetle: The Beetle can move one space at a time like the Queen Bee, but it
   also has the unique ability to climb on top of other pieces. This makes it
   a very versatile and valuable piece.

10. Spider: The Spider must move exactly three spaces per turn, which can be
    limiting but also allows for strategic positioning. It cannot backtrack in
    the 3-space move.

11. Grasshopper: The Grasshopper jumps over other pieces and can quickly move
    across the board. This makes it a valuable piece for both offense and
    defense.

12. Ant: The Ant can move to any unoccupied space on the board, making it the
    most mobile piece.

13. Ladybug (expansion): The Ladybug moves three spaces per turn, two on top of
    the Hive, and one down. It can't end its movement on top of the Hive, which
    limits its versatility.

14. Mosquito (expansion): The Mosquito takes on the movement abilities of any
    piece it touches, making it potentially very versatile.

15. Pillbug (expansion): The Pillbug can move one space at a time, or it can
    move an adjacent unstacked piece (friend or foe) to another empty space
    around itself.

16. Game End Rule: The game ends when a queen bee is surrounded on all six
    sides by pieces of any color, with that player losing the game.
