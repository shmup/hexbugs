CREATE TRIGGER verify_bug_id_before_transaction
BEFORE INSERT ON transactions
FOR EACH ROW
WHEN NEW.transaction_type_id = 'add'
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

CREATE VIEW game_history AS
SELECT 
    t.game_id,
    t.player_id,
    p.name AS player_name,
    tt.type AS action_type,
    b.name AS bug_name,
    json_extract(t.action, '$.x') AS x,
    json_extract(t.action, '$.y') AS y,
    t.timestamp
FROM 
    transactions t
JOIN 
    players p ON t.player_id = p.id
JOIN 
    bugs b ON json_extract(t.action, '$.bug_id') = b.id
JOIN 
    transaction_types tt ON t.transaction_type_id = tt.id
WHERE 
    tt.type IN ('add', 'move')
ORDER BY 
    t.timestamp;

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
     (SELECT type FROM transaction_types WHERE id = NEW.transaction_type_id) IN ('add', 'move')
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
