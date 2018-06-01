import unittest
from boggle.board import Board

class TestBoard(unittest.TestCase):
    def setUp(self):
        self.boardClass = Board()
        self.test_board_string = "ACEDLUG*E*HTGAFK"
        self.test_board = [["a", "c", "e", "d"],
                           ["l", "u", "g", "*"],
                           ["e", "*", "h", "t"],
                           ["g", "a", "f", "k"]
                           ]

    def test_board_from_string(self):
        self.boardClass = self.boardClass.from_string(self.test_board_string)
        self.assertListEqual(self.boardClass.board,
                             [
                                 ["a", "c", "e", "d"],
                                 ["l", "u", "g", "*"],
                                 ["e", "*", "h", "t"],
                                 ["g", "a", "f", "k"]
                             ])

    def test_board_id_from_string(self):
        self.boardClass.board = self.test_board
        self.assertEqual(self.boardClass.to_string(),"acedlug*e*htgafk")


if __name__ == "__main__":
    unittest.main()