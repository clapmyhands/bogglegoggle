import uuid
from enum import Enum
from boggle.board import Board

class Match:
    new_match = "INSERT INTO match VALUES (?, ?, NULL, '', 0, NULL, '', 0)"
    first_finish = "UPDATE match SET p1_name = ?, p1_words = ?, p1_score = ? WHERE match_id = ?"
    second_finish = "UPDATE match SET p2_name = ?, p2_words = ?, p2_score = ? WHERE match_id = ?"
    get_match = "SELECT * FROM match WHERE match_id = ?"

    def __init__(self, match_id:str, boardString:str,
                 p1_name=None, p1_words=None, p1_score=None,
                 p2_name=None, p2_words=None, p2_score=None):
        self.match_id = match_id
        self.board_string = boardString
        self.p1_name = p1_name
        self.p1_words = p1_words.split(',') if p1_words else [""]
        self.p1_score = int(p1_score) if p1_score else 0
        self.p2_name = p2_name
        self.p2_words = p2_words.split(',') if p2_words else [""]
        self.p2_score = int(p2_score) if p2_score else 0



    def get_match_id(self):
        return self.match_id

    def get_board_string(self):
        return self.board_string

    def is_finished(self):
        return True if self.first_finished() and self.second_finished() else False

    def first_finished(self):
        return True if self.p1_name else False

    def second_finished(self):
        return True if self.p2_name else False


    def to_dict(self):
        myDict = {
            "match_id": self.match_id,
            "board_string": self.board_string,
            "p1_name": self.p1_name,
            "p1_words": self.p1_words,
            "p1_score": self.p1_score,
            "p2_name": self.p2_name,
            "p2_words": self.p2_words,
            "p2_score": self.p2_score
        }
        return myDict

    @staticmethod
    def generate_match_id():
        return str(uuid.uuid4())

    def update_match(self, match_id, first:bool, words:list, name:str):

        pass

    def get_match_id(self):
        return self.match_id

    def get_board(self):
        return self.board