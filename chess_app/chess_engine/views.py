from django.http import HttpResponse, HttpRequest
from django.shortcuts import render

from chess_app.chess_engine.models.game import Game
from chess_app.chess_engine.models.playerBase import InitPlayer
# Create your views here.
def index(request):
    return HttpResponse("Hello world, you re at the chess engine index")

def createGame(request: HttpRequest):
    black = InitPlayer("manu", False)
    white = InitPlayer("random", True)
    game = Game(black, white)
    return game.getBoardImage()