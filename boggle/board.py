import hashlib
from boggle import ASSET_PATH

class Board:
    def __init__(self):
        self.board = None
        self.board_id = None

    def from_string(self, board_string):
        board_1d = list(board_string.strip().lower())
        # hardcoded 4x4 for now
        m = 4
        n = len(board_1d)//m
        assert m*n == len(board_1d)
        self.board = [board_1d[(i*m):(i*m)+n] for i in range(m)]
        return self

    def load_from_database(self, board_id:str):
        pass

    def __str__(self):
        assert self.board is not None # is this correct? hmm
        return "".join(j for i in self.board for j in i)

    def to_string(self):
        return str(self)

    @staticmethod
    def load_from_file(fp, redisConn):
        with open(fp, 'r', encoding="utf-8") as boardFile:
            boards = [i.strip().lower() for i in boardFile.readlines()]

        redisConn.sadd("boards-list", *boards) # move constant

