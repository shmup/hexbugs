import unittest
import asyncio
from unittest.mock import Mock
from hexbugs.mind.manager import GameManager

class TestGameManager(unittest.TestCase):
    def setUp(self):
        self.gm = GameManager()
        self.loop = asyncio.get_event_loop()

    def test_handle_join_message(self):
        message = {'action': 'join'}
        self.gm.join_game = Mock()
        self.loop.run_until_complete(self.gm.handle_message(message))
        self.gm.join_game.assert_called_once()

    def test_handle_move_message(self):
        message = {'action': 'move'}
        self.gm.move_piece = Mock()
        self.loop.run_until_complete(self.gm.handle_message(message))
        self.gm.move_piece.assert_called_once()

if __name__ == '__main__':
    unittest.main()
