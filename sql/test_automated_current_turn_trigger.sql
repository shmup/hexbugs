INSERT INTO players (name) VALUES ('Weasel'), ('Bravd');

INSERT INTO games (current_turn) VALUES ((SELECT id FROM players WHERE name = 'Weasel'));

INSERT INTO game_players (game_id, player_id)
VALUES
    ((SELECT id FROM games), (SELECT id FROM players WHERE name = 'Weasel')),
    ((SELECT id FROM games), (SELECT id FROM players WHERE name = 'Bravd'));

SELECT "Weasel adds a bug";
INSERT INTO transactions (game_id, player_id, transaction_type_id, action)
VALUES
    ((SELECT id FROM games), (SELECT id FROM players WHERE name = 'Weasel'), (SELECT id FROM transaction_types WHERE name = 'add'), '{"bug": 1}');

SELECT 'Current turn: ' || current_turn AS current_turn_label FROM games;

SELECT "Bravd adds a bug";
INSERT INTO transactions (game_id, player_id, action)
VALUES
    ((SELECT id FROM games), (SELECT id FROM players WHERE name = 'Bravd'), '{"type": "add", "bug": 2}');

SELECT 'Current turn: ' || current_turn AS current_turn_label FROM games;
