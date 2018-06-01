import os

from boggle import ASSET_PATH, DB_PATH
from boggle.board import Board
from boggle.dictionary import Dictionary
from boggle.boggleGame import BoggleGame
from boggle.match import Match

from flask import Flask, jsonify, abort, request, Response, render_template
import redis


app = Flask(__name__)
redisConn = redis.StrictRedis(host='localhost', port=6379, db=0)

# move this to config
dictionaryFP = os.path.join(ASSET_PATH, "dictionary.txt")
dictionary = Dictionary(dictionaryFP)

boardFP = os.path.join(ASSET_PATH, 'TestBoard.txt')
Board.load_from_file(boardFP, redisConn)

boggleGame = BoggleGame(dictionary, redisConn, DB_PATH)




@app.route("/status")
def status():
    return "Health Check"

@app.route("/")
@app.route("/boggle/game", methods=['GET'])
def play_single():
    return render_template('boggle-game.html')

# return random board from board cache
@app.route("/api/v1.0/boggle/boards", methods=['GET'])
def get_random_board():
    board_string = boggleGame.get_random_board_string()
    response = jsonify({"board_string": board_string})
    return response

# find word in selected board
# return score based on char length
@app.route("/api/v1.0/boggle/boards/<string:board_string>/word/<string:word>", methods=['GET'])
def find_word(board_string:str, word:str):
    # hardcoded 4x4 size for now, can add POST method with json data later if needed
    if(len(board_string)!=16):
        abort(400)

    is_found = boggleGame.find_word(board_string, word)
    score = len(word) if is_found else 0 # might want to move this to database
    return jsonify({"score": score, "word": word})


# get match status
@app.route("/api/v1.0/boggle/matches/<string:match_id>", methods=['GET'])
def get_match(match_id:str):
    match_status = boggleGame.get_match_status(match_id)

    if match_status is None:
        abort(400)

    if match_status["status"] == "ongoing":
        match_status = {
            "match_id": match_status["match_id"],
            "status": "ongoing"
        }

    return jsonify(match_status)

# create a new match
# return match_id
@app.route("/api/v1.0/boggle/matches", methods=['POST'])
def new_match():
    match_id = boggleGame.create_new_match()
    return jsonify({"match_id": match_id})

# finish a match
# give words used, and name?
@app.route("/api/v1.0/boggle/matches/<string:match_id>", methods=['PUT'])
def player_finish_match(match_id:str):
    request_data = request.get_json()
    name = request_data['name']
    words = request_data['words']
    match_status = boggleGame.update_match(match_id, name, words)
    if match_status is None:
        abort(400) # match is already completed
    return jsonify(match_status)

# return board, player status
@app.route("/api/v1.0/boggle/matches/<string:match_id>/session", methods=['POST'])
def start_match(match_id:str):
    board_string = boggleGame.start_match(match_id)
    if board_string is None:
        abort(400) # match is already completed
    return jsonify({"match_id":match_id ,"board_string": board_string})

@app.route("/api/v1.0/boggle/boards", methods=['POST'])
def generate_board():
    pass

if __name__ == '__main__':
    app.run()
