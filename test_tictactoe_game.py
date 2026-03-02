import unittest

from game_logic import TicTacToeGame


class TicTacToeGameTests(unittest.TestCase):
    def test_alternates_player_after_valid_move(self):
        game = TicTacToeGame()
        self.assertTrue(game.make_move(0))
        self.assertEqual(game.board[0], "X")
        self.assertEqual(game.current_player, "O")

    def test_rejects_move_on_filled_cell(self):
        game = TicTacToeGame()
        self.assertTrue(game.make_move(4))
        self.assertFalse(game.make_move(4))

    def test_detects_winner(self):
        game = TicTacToeGame()
        game.make_move(0)  # X
        game.make_move(3)  # O
        game.make_move(1)  # X
        game.make_move(4)  # O
        game.make_move(2)  # X thắng hàng đầu

        self.assertEqual(game.winner, "X")
        self.assertFalse(game.is_draw)

    def test_detects_draw(self):
        game = TicTacToeGame()
        # Trạng thái hòa: X O X / X O O / O X X
        sequence = [0, 1, 2, 3, 5, 4, 6, 8, 7]
        for move in sequence:
            self.assertTrue(game.make_move(move))

        self.assertIsNone(game.winner)
        self.assertTrue(game.is_draw)


if __name__ == "__main__":
    unittest.main()
