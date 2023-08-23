CREATE TABLE IF NOT EXISTS bugs (
    id INTEGER PRIMARY KEY,
    name TEXT
);

INSERT INTO bugs (name)
VALUES
    ('Queen'), ('Beetle'), ('Spider'), ('Grasshopper'), ('Ant'), ('Ladybug'), ('Mosquito'), ('Pillbug'),
    ('Queen'), ('Beetle'), ('Spider'), ('Grasshopper'), ('Ant'), ('Ladybug'), ('Mosquito'), ('Pillbug');

CREATE TABLE IF NOT EXISTS players (
    id INTEGER PRIMARY KEY,
    name TEXT
);

CREATE TABLE IF NOT EXISTS games (
    id INTEGER PRIMARY KEY,
    current_turn INTEGER,
    game_over INTEGER DEFAULT 0,
    state TEXT, /* json or a string. re-renders a page from nothing */
    FOREIGN KEY(current_turn) REFERENCES players(id)
);

CREATE TABLE IF NOT EXISTS game_players (
    game_id INTEGER,
    player_id INTEGER,
    FOREIGN KEY(game_id) REFERENCES games(id),
    FOREIGN KEY(player_id) REFERENCES players(id)
);

CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY,
    game_id INTEGER,
    player_id INTEGER,
    action TEXT, /* json or string, a player action or changing game state */
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(game_id) REFERENCES games(id),
    FOREIGN KEY(player_id) REFERENCES players(id)
);

CREATE TRIGGER verify_bug_id_before_transaction
BEFORE INSERT ON transactions
FOR EACH ROW
WHEN json_extract(NEW.action, '$.type') = 'add'
BEGIN
   SELECT RAISE(ABORT, 'Invalid bug_id')
   WHERE NOT EXISTS (
      SELECT 1 FROM bugs WHERE id = json_extract(NEW.action, '$.bug_id')
   );
END;
CREATE VIEW IF NOT EXISTS game_view AS
SELECT
    g.id AS game_id,
    g.game_over,
    g.state,
    p1.name AS current_turn,
    GROUP_CONCAT(p2.name, ', ') AS players
FROM
    games g
JOIN
    players p1 ON g.current_turn = p1.id
JOIN
    game_players gp ON g.id = gp.game_id
JOIN
    players p2 ON gp.player_id = p2.id
GROUP BY
    g.id;

CREATE TRIGGER update_turn_after_transaction
AFTER INSERT ON transactions
BEGIN
   UPDATE games
   SET current_turn = (
     SELECT player_id
     FROM game_players
     WHERE game_id = NEW.game_id
     AND (
       current_turn IS NULL OR
       player_id != current_turn
     )
     ORDER BY player_id ASC
     LIMIT 1
   )
   WHERE id = NEW.game_id
   AND (
     json_extract(NEW.action, '$.type') = 'add' OR
     json_extract(NEW.action, '$.type') = 'move'
   );
END;

CREATE TRIGGER set_first_turn_after_second_player_added
AFTER INSERT ON game_players
BEGIN
   UPDATE games
   SET current_turn = (
     SELECT player_id
     FROM (
       SELECT player_id
       FROM game_players
       WHERE game_id = NEW.game_id
       LIMIT 1
     )
   )
   WHERE id = NEW.game_id
   AND (
     SELECT COUNT(player_id)
     FROM game_players
     WHERE game_id = NEW.game_id
   ) = 2;
END;
