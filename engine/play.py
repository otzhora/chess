# Taken from https://github.com/geohot/twitchchess
import base64
import traceback
import os

import chess
import chess.svg
from flask import Flask, Response, request

from engine.value_functions import *
from engine.engines import *


app = Flask(__name__, static_folder="../static")

board = chess.Board()
engine = MinMaxEngine(value_function=ClassicValue, max_depth=3)


def to_svg():
    return base64.b64encode(chess.svg.board(board=board).encode('utf-8')).decode('utf-8')


@app.route("/")
def hello():
    ret = open("../index.html").read()
    return ret.replace('start', board.fen())


def computer_move():
    # computer move
    val, move = engine(board)
    print(board.turn, "moving", move)
    board.push(move)


@app.route("/selfplay")
def selfplay():
    ret = '<html><head>'
    # self play
    i = 0
    while not board.is_game_over():
        print(i)
        i += 1
        computer_move()
        ret += '<img width=600 height=600 src="data:image/svg+xml;base64,%s"></img><br/>' % to_svg()
    print(board.result())

    return ret


# move given in algebraic notation
@app.route("/move")
def move():
    if not board.is_game_over():
        move = request.args.get('move', default="")
        if move is not None and move != "":
            print("human moves", move)
            try:
                board.push_san(move)
                computer_move()
            except Exception:
                traceback.print_exc()
            response = app.response_class(
                response=board.fen(),
                status=200
            )
            return response
    else:
        print("GAME IS OVER")
        response = app.response_class(
            response="game over",
            status=200
        )
        return response
    return hello()


# moves given as coordinates of piece moved
@app.route("/move_coordinates")
def move_coordinates():
    if not board.is_game_over():
        source = int(request.args.get('from', default=''))
        target = int(request.args.get('to', default=''))
        promotion = True if request.args.get('promotion', default='') == 'true' else False

        move = board.san(chess.Move(source, target, promotion=chess.QUEEN if promotion else None))

        if move is not None and move != "":
            print("human moves", move)
            try:
                board.push_san(move)
                computer_move()
            except Exception:
                traceback.print_exc()
        response = app.response_class(
            response=board.fen(),
            status=200
        )
        return response

    print("GAME IS OVER")
    response = app.response_class(
        response="game over",
        status=200
    )
    return response


@app.route("/newgame")
def newgame():
    board.reset()
    response = app.response_class(
        response=board.fen(),
        status=200
    )
    return response


if __name__ == "__main__":
    if os.getenv("SELFPLAY") is not None:
        while not board.is_game_over():
            computer_move()
            print(board)
        print(board.result())
    else:
        app.run(debug=True)
