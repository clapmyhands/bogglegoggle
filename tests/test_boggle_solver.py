from boggle.boggleGame import BoggleGame, BoggleSolver
from boggle.dictionary import Dictionary
from boggle.board import Board
import unittest

class TestBoggleSolver(unittest.TestCase):
    def setUp(self):
        self.Dictionary = Dictionary()
        self.Dictionary.trie = {'e': {'i': {'g': {'h': {'t': {'leave': True}}}}},
                              'h': {'u': {'g': {'e': {'leave': True},
                                                'leave': True}}}}
        self.Board = Board()
        self.Board.board = [["a", "c", "e", "d"],
                            ["l", "u", "g", "*"],
                            ["e", "*", "h", "t"],
                            ["g", "a", "f", "k"]
                            ]

        self.BoggleSolver = BoggleSolver(self.Dictionary)
        self.BoggleSolver.set_board(self.Board)

    def test_outside_board(self):
        self.assertTrue(self.BoggleSolver.outside_board(-1, 0))
        self.assertTrue(self.BoggleSolver.outside_board(0, -1))
        self.assertTrue(self.BoggleSolver.outside_board(4, 0))
        self.assertTrue(self.BoggleSolver.outside_board(0, 4))

    def test_inside_board(self):
        self.assertFalse(self.BoggleSolver.outside_board(2, 2))

    def test_next_moves(self):
        self.assertListEqual(
            self.BoggleSolver.next_move(0, 0),
            [(0,1), (1,1), (1,0)])

        self.assertListEqual(
            self.BoggleSolver.next_move(2, 2),
            [(1,2), (1,3), (2,3), (3,3), (3,2), (3,1), (2,1), (1,1)])

    def test_solve(self):
        result = self.BoggleSolver.solve()
        result.sort()
        self.assertListEqual(result, ["eight", "hug", "huge"])

if __name__ == '__main__':
    unittest.main()