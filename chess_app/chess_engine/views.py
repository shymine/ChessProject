import chess 
import traceback

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
    white = InitPlayer("random", True)
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
    move = request.POST.get("move")
    game = GAME[0]
    results = {}
    if game.isCheckmate() or game.isDraw()[0]:
        results = {
        "image": game.getBoardImage(),
        "white": game.players[True].name,
        "black": game.players[False].name,
        "current": game.players[game.board.turn],
        "history": game.getHistory(),
        "draw": game.isDraw(),
        "win": game.isCheckmate(),
        "error_message": "",
        }
    else:
        if game.players[game.currentColor()].is_ai:
            results = _ais(game)
        else:
            results = _player(move, game)

    
    return render(request, "chess_engine/game.html", results)

def _player(move: str | None, game: Game):  
    error_message = ""
    if move is None:
        error_message = "no move present"
    else:
        try:
            uci_move = chess.Move.from_uci(move)
            if uci_move in game.legalMoves():
                game.play(uci_move)
            else:
                raise Exception("Illegal Move")
        except Exception as err:
            error_message = err
            traceback.print_exc()
    return {
        "image": game.getBoardImage(),
        "white": game.players[True].name,
        "black": game.players[False].name,
        "current": game.players[game.board.turn],
        "history": game.getHistory(),
        "draw": game.isDraw(),
        "win": game.isCheckmate(),
        "error_message": error_message,
        }

def _ais(game: Game):
    error_message = ""
    game.play()
    return {
        "image": game.getBoardImage(),
        "white": game.players[True].name,
        "black": game.players[False].name,
        "current": game.players[game.board.turn],
        "history": game.getHistory(),
        "draw": game.isDraw(),
        "win": game.isCheckmate(),
        "error_message": error_message,
        }