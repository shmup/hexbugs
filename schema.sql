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

/* CREATE TRIGGER check_game_player_before_insert */
/* BEFORE INSERT ON transactions */
/* FOR EACH ROW */
/* BEGIN */
/*   SELECT CASE */
/*     WHEN (SELECT COUNT(*) FROM game_players WHERE game_id = NEW.game_id AND player_id = NEW.player_id) = 0 THEN */
/*       RAISE(FAIL, "Transaction involves a player not in the game") */
/*   END; */
/* END; */

/* CREATE TRIGGER IF NOT EXISTS enforce_current_turn */
/* BEFORE INSERT ON games */
/* FOR EACH ROW */
/* BEGIN */
/*     SELECT CASE */
/*         WHEN (SELECT COUNT(*) FROM game_players WHERE game_id = NEW.id AND player_id = NEW.current_turn) = 0 THEN */
/*         RAISE(ABORT, 'Current turn must be one of the players') */
/*     END; */
/* END; */

/* CREATE TRIGGER IF NOT EXISTS enforce_current_turn */
/* BEFORE INSERT ON games */
/* FOR EACH ROW */
/* BEGIN */
/*     SELECT CASE */
/*         WHEN (SELECT COUNT(*) FROM game_players WHERE game_id = NEW.id AND player_id = NEW.current_turn) != 1 THEN */
/*         RAISE(ABORT, 'Current turn must be one of the players') */
/*     END; */
/* END; */

/* CREATE TABLE IF NOT EXISTS action_codes ( */
/*     code INTEGER PRIMARY KEY UNIQUE, */
/*     description TEXT */
/* ); */

/* INSERT OR IGNORE INTO action_codes (code, description) VALUES */
/*     (0, 'Player loses'), */
/*     (1, 'Player wins'); */

/* CREATE TRIGGER IF NOT EXISTS enforce_player_in_game */
/* BEFORE INSERT ON transactions */
/* FOR EACH ROW */
/* BEGIN */
/*     SELECT CASE */
/*         WHEN (SELECT player1_id FROM games WHERE id = NEW.game_id) != NEW.player_id AND */
/*              (SELECT player2_id FROM games WHERE id = NEW.game_id) != NEW.player_id THEN */
/*         RAISE(ABORT, 'Player must be in the current game') */
/*     END; */
/* END; */

/* CREATE TRIGGER IF NOT EXISTS enforce_different_players */
/* BEFORE INSERT ON games */
/* FOR EACH ROW */
/* BEGIN */
/*     SELECT CASE */
/*         WHEN NEW.player1_id = NEW.player2_id THEN */
/*         RAISE(ABORT, 'Player1 and Player2 cannot be the same player') */
/*     END; */
/* END; */

/* CREATE TRIGGER IF NOT EXISTS enforce_two_players */
/* BEFORE INSERT ON transactions */
/* FOR EACH ROW */
/* BEGIN */
/*     SELECT CASE */
/*         WHEN (SELECT player1_id FROM games WHERE id = NEW.game_id) IS NULL OR */
/*              (SELECT player2_id FROM games WHERE id = NEW.game_id) IS NULL THEN */
/*         RAISE(ABORT, 'Game must have two distinct players before starting') */
/*     END; */
/* END; */

/* CREATE TRIGGER IF NOT EXISTS enforce_alternating_turns */
/* BEFORE INSERT ON transactions */
/* FOR EACH ROW */
/* BEGIN */
/*     SELECT CASE */
/*         WHEN (SELECT player_id FROM transactions WHERE game_id = NEW.game_id ORDER BY timestamp DESC LIMIT 1) = NEW.player_id THEN */
/*         RAISE(ABORT, 'Player cannot make two moves in a row') */
/*     END; */
/* END; */

/* CREATE TRIGGER IF NOT EXISTS enforce_game_over */
/* BEFORE INSERT ON transactions */
/* FOR EACH ROW */
/* BEGIN */
/*     SELECT CASE */
/*         WHEN (SELECT game_over FROM games WHERE id = NEW.game_id) = 1 THEN */
/*         RAISE(ABORT, 'Game has already ended') */
/*     END; */
/* END; */

/* CREATE TRIGGER IF NOT EXISTS enforce_different_actions */
/* BEFORE INSERT ON transactions */
/* FOR EACH ROW */
/* BEGIN */
/*     SELECT CASE */
/*         WHEN (SELECT action FROM transactions WHERE game_id = NEW.game_id ORDER BY timestamp DESC LIMIT 1) = NEW.action THEN */
/*         RAISE(ABORT, 'Player cannot perform the same action twice in a row') */
/*     END; */
/* END; */

/* CREATE TRIGGER IF NOT EXISTS enforce_player_turn */
/* BEFORE INSERT ON transactions */
/* FOR EACH ROW */
/* BEGIN */
/*     SELECT CASE */
/*         WHEN (SELECT current_turn FROM games WHERE id = NEW.game_id) != NEW.player_id THEN */
/*         RAISE(ABORT, 'It is not the player''s turn') */
/*     END; */
/* END; */

/* CREATE TRIGGER IF NOT EXISTS enforce_one_move_per_turn */
/* BEFORE INSERT ON transactions */
/* FOR EACH ROW */
/* BEGIN */
/*     SELECT CASE */
/*         WHEN (SELECT player_id FROM transactions WHERE game_id = NEW.game_id ORDER BY timestamp DESC LIMIT 1) = NEW.player_id THEN */
/*         RAISE(ABORT, 'Player cannot make multiple moves in one turn') */
/*     END; */
/* END; */

/* CREATE TRIGGER IF NOT EXISTS update_game_state */
/* AFTER INSERT ON transactions */
/* FOR EACH ROW */
/* BEGIN */
/*     UPDATE games */
/*     SET state = (SELECT action FROM transactions WHERE game_id = NEW.game_id ORDER BY timestamp DESC LIMIT 1) */
/*     WHERE id = NEW.game_id; */
/* END; */

/* CREATE TRIGGER IF NOT EXISTS switch_turns */
/* AFTER INSERT ON transactions */
/* FOR EACH ROW */
/* BEGIN */
/*     UPDATE games */
/*     SET current_turn = CASE WHEN current_turn = player1_id THEN player2_id ELSE player1_id END */
/*     WHERE id = NEW.game_id; */
/* END; */

/* CREATE TRIGGER IF NOT EXISTS game_over */
/* AFTER INSERT ON transactions */
/* FOR EACH ROW */
/* WHEN NEW.action_code = 1 -- 'Player wins' is represented by 1 */
/* BEGIN */
/*     UPDATE games */
/*     SET game_over = 1 */
/*     WHERE id = NEW.game_id; */
/* END; */
