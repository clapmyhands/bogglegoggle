from boggle.board import Board
from boggle.dictionary import Dictionary

class BoggleSolver:
    def __init__(self, dictionary:Dictionary):
        self.trieRoot = dictionary.get_trie()
        self.adjacent = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
        self.board = None
        self.m = None
        self.n = None
        self.usedBoard = None
        self.origin_point = None
        self.solution_set = set()

    def set_board(self, board:Board):
        self.board = board.board
        self.m = len(self.board)
        self.n = len(self.board[0])
        self.usedBoard = [[False for j in range(self.n)] for i in range(self.m)]
        self.origin_point = [(i, j) for i in range(self.m) for j in range(self.n)]

    def outside_board(self, i, j):
        return i < 0 or j < 0 or i >= self.m or j >= self.n

    def next_move(self, i, j): # find next valid moves
        moves = ((i + y, j + x) for (y, x) in self.adjacent) # find all movement
        moves = [(y,x) for (y,x) in moves if not self.outside_board(y, x)] # only inside board
        moves = [(y,x) for (y,x) in moves if not self.usedBoard[y][x]] # only to unused cell
        return moves

    def solve(self):
        for (i,j) in self.origin_point:
            self.solve_rec(i,j,self.trieRoot,"")
        result = list(self.solution_set)
        return result

    def solve_rec(self, i, j, trieNode, word):
        current_char = self.board[i][j]
        if "leave" in trieNode:
            self.solution_set.add(word)

        self.usedBoard[i][j] = True
        if current_char == '*':
            for key in trieNode:
                if key == "leave":
                    continue
                nextWord = word+key
                nextNode = trieNode[key]
                nextMoves = self.next_move(i,j)
                for (y,x) in nextMoves:
                    self.solve_rec(y,x,nextNode,nextWord)
        elif current_char in trieNode:
            nextWord = word + current_char
            nextNode = trieNode[current_char]
            nextMoves = self.next_move(i, j)
            for (y, x) in nextMoves:
                self.solve_rec(y, x, nextNode, nextWord)
        self.usedBoard[i][j] = False