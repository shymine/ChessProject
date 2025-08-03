import chess 

from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.template import loader

from chess_engine.models.game import Game
from chess_engine.models.playerBase import InitPlayer

GAME: list[Game] = []
# Create your views here.
def index(request):
    return render(request, "chess_engine/index.html")

def createGame(request: HttpRequest):
    black = InitPlayer("manu", False)
    white = InitPlayer("random", False)
    game = Game(black, white)
    GAME.append(game)
    return render(request, "chess_engine/game.html", {
        "image": game.getBoardImage(),
        "white": game.players[True].name,
        "black": game.players[False].name,
        "current": game.players[game.board.turn],
        "history": game.getHistory()
        })

def play(request: HttpRequest):
    move = chess.Move.from_uci("e2e4")
    GAME[0].play(move)
    game = GAME[0]
    return render(request, "chess_engine/game.html", {
        "image": game.getBoardImage(),
        "white": game.players[True].name,
        "black": game.players[False].name,
        "current": game.players[game.board.turn],
        "history": game.getHistory()
        })

