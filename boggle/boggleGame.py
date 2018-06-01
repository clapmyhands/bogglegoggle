from boggle.board import Board
from boggle.dictionary import Dictionary
from boggle.match import Match
from boggle.boggleSolver import BoggleSolver
import uuid

import redis, sqlite3


class BoggleGame:
    def __init__(self, dictionary:Dictionary, redisConn:redis.StrictRedis, dbName):
        self.BoggleSolver = BoggleSolver(dictionary)
        self.redis = redisConn
        self.db_name = dbName


    def get_random_board_string(self):
        board_string = self.redis.srandmember('boards-list').decode('utf-8') #move this 'boards' to config or constant
        return board_string

    def solve_board(self, boardClass:Board):
        self.BoggleSolver.set_board(boardClass)
        result = self.BoggleSolver.solve()

        # save word list in redis
        boardName = "boards:{}".format(boardClass.to_string())
        self.redis.sadd(boardName, *result)

        return result

    def find_word(self, board_string:str, word:str):
        boardName = "boards:{}".format(board_string)
        if self.redis.exists(boardName):
            is_valid = self.redis.sismember(boardName, word)
        else:
            result = self.solve_board(Board().from_string(board_string))
            is_valid = True if word in result else False

        return is_valid

    def count_score(self, board_string:str, words:list):
        boardName = "boards:{}".format(board_string)
        score = 0
        if self.redis.exists(boardName):
            for word in words:
                score += len(word) if self.redis.sismember(boardName, word) else 0
        return score

    def create_new_match(self):
        match_id = Match.generate_match_id()
        board_string = self.get_random_board_string()
        with sqlite3.connect(self.db_name) as conn:
            with conn:
                cursor = conn.cursor()
                stmt = Match.new_match
                param = (match_id, board_string)
                cursor.execute(stmt, param)
        self.redis.set("matches:{}".format(match_id), board_string)
        return match_id

    def start_match(self, match_id:str):
        # matchesName = "matches:{}".format(match_id)
        # board_string = self.redis.get(matchesName).decode('utf-8')
        #
        # if board_string is None:
        #     match_status = self.get_match_status(match_id)
        #     board_string = match_status["board_string"]
        match = self.get_match_status(match_id, False)
        if match.is_finished():
            return None

        return match.board_string

    def update_match(self, match_id, name:str, words:list):
        match = self.get_match_status(match_id, False)
        if match.is_finished():
            return None

        match_status = match.to_dict()
        board_string = match.board_string

        score = self.count_score(board_string, words)
        words_string = ",".join(words)

        match_status = {
            "board_string": match.board_string,
            "match_id": match.match_id
        }
        if not match.first_finished():
            stmt = Match.first_finish
            match_status["status"] = "ongoing"
        else:
            stmt = Match.second_finish
            match_status["status"] = "finished"

        with sqlite3.connect(self.db_name) as conn:
            with conn:
                cursor = conn.cursor()
                param = (name, words_string, score, match_id)
                cursor.execute(stmt, param)

        return match_status



    def get_match_status(self, match_id:str, as_dict=True):
        with sqlite3.connect(self.db_name) as conn:
            with conn:
                cursor = conn.cursor()
                stmt = Match.get_match
                param = (match_id,)
                cursor.execute(stmt, param)
                row = cursor.fetchone()

                if row is None:
                    return None

                match = Match(*row)
                if as_dict:
                    match_status = match.to_dict()
                    match_status["status"] = "finished" if match.is_finished() else "ongoing"
                    return match_status
                else:
                    return match


    def generate_new_board(self):
        pass
