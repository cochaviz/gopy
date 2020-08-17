import unittest

from go import component
from go import rulebooks

class TestRulebook(unittest.TestCase):
    
    def setUp(self):
        self.board = component.Board(size=13)
        self.rulebook = rulebooks.Standard()

        self.white_stones = []
        self.black_stones = []

        for _ in range(5):
            self.white_stones.append(component.Stone(1))
            self.black_stones.append(component.Stone(0))

    def test_captured_group(self):
        self.board.place(self.white_stones[0], 0, 1)
        _, endangered_group = self.board.place(self.black_stones[0], 0, 0)
        _, current_group = self.board.place(self.white_stones[1], 1, 0)
        legal_move, captured_groups = self.rulebook.check_current_move([], self.board, current_group)

        print(self.board)

        self.assertTrue(legal_move)
        self.assertTrue(endangered_group in captured_groups)

    def test_illegal_move(self):
        self.board.place(self.white_stones[0], 0, 1)
        self.board.place(self.white_stones[1], 1, 0)
        _, current_group = self.board.place(self.black_stones[0], 0, 0)
        legal_move, captured_groups = self.rulebook.check_current_move([], self.board, current_group)
        
        self.assertFalse(legal_move)
        self.assertEquals(current_group, captured_groups[0])

    def test_ko_rule(self):
        self.board.place(self.white_stones[0], 0, 1)
        self.board.place(self.white_stones[1], 1, 0)
        self.board.place(self.white_stones[2], 2, 1)
        self.board.place(self.white_stones[3], 1, 2)
        self.board.place(self.black_stones[0], 2, 0)
        self.board.place(self.black_stones[1], 2, 2)
        self.board.place(self.black_stones[2], 3, 1)

        states = set()
        states.add(hash(self.board))

        _, current_group = self.board.place(self.black_stones[4], 1, 1)
        legal_move, captured_groups = self.rulebook.check_current_move(states, self.board, current_group)
        states.add(hash(self.board))
        
        self.assertTrue(legal_move)

        for group in captured_groups:
            self.board.remove_group(group) 
    
        print(self.board)

        _, current_group = self.board.place(self.white_stones[4], 2, 1)
        legal_move, _ = self.rulebook.check_current_move(states, self.board, current_group)
        states.add(hash(self.board))
        

        print(self.board)
        self.assertFalse(legal_move)


if __name__ == "__main__":
    unittest.main()
