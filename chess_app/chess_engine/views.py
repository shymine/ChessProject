import chess 

from django.http import HttpResponse, HttpRequest
from django.shortcuts import render

from chess_engine.models.game import Game
from chess_engine.models.playerBase import InitPlayer

GAME: list[Game] = []
# Create your views here.
def index(request):
    return HttpResponse("Hello world, you re at the chess engine index")

def createGame(request: HttpRequest):
    black = InitPlayer("manu", False)
    white = InitPlayer("random", False)
    game = Game(black, white)
    GAME.append(game)
    return HttpResponse(game.getBoardImage())

def play(request: HttpRequest):
    move = chess.Move.from_uci("e2e4")
    GAME[0].play(move)
    return HttpResponse(GAME[0].getBoardImage())

