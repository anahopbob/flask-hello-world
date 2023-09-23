import json
import logging
from typing import Dict, List

from flask import request

from routes import app

logger = logging.getLogger(__name__)


maze = None
width = 0
current_position = None

def initialize_maze(data):
    global maze, width, current_position
    maze = data["nearby"]
    width = data["mazeWidth"]
    current_position = (1, 1) 

def is_valid_move(x, y):
    logging.info("NEW MOVE IS {}".format(maze[x][y]))

    return 0 <= x < width and 0 <= y < width and maze[x][y] != 0

def get_next_move(data):
    initialize_maze(data)
    possible_moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    for move in possible_moves:
        x, y = current_position[0] + move[0], current_position[1] + move[1]

        if is_valid_move(x, y):
            if move == (0, 1):
                return "down"
            elif move == (1, 0):
                return "right"
            elif move == (0, -1):
                return "up"
            elif move == (-1, 0):
                return "left"
    return "respawn"

@app.route('/maze', methods=['POST'])
def evaluate_maze():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))

    res: {str: str} = {"playerAction" : get_next_move(data)}

    logging.info("My result :{}".format(res))
    return json.dumps(res)