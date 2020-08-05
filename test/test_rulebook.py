import unittest

from go import component
from go import rulebooks

class TestRulebook(unittest.TestCase):
    
    def setUp(self):
        self.board = component.Board(size=13)
        self.rulebook = rulebooks.Standard()

        self.white_stones = []
        self.black_stones = []

        for _ in range(3):
            self.white_stones.append(component.Stone(1))
            self.black_stones.append(component.Stone(0))

    def test_captured_group(self):
        self.board.place(self.white_stones[0], 0, 1)
        _, endangered_group = self.board.place(self.black_stones[0], 0, 0)
        _, current_group = self.board.place(self.white_stones[1], 1, 0)
        legal_move, captured_groups = self.rulebook.check_current_move(self.board, current_group)

        self.assertTrue(legal_move)
        self.assertEquals(endangered_group, captured_groups[0])

    def test_illegal_move(self):
        self.board.place(self.white_stones[0], 0, 1)
        self.board.place(self.white_stones[1], 1, 0)
        _, current_group = self.board.place(self.black_stones[0], 0, 0)
        legal_move, captured_groups = self.rulebook.check_current_move(self.board, current_group)
        
        self.assertFalse(legal_move)
        self.assertEquals(current_group, captured_groups[0])

if __name__ == "__main__":
    unittest.main()
