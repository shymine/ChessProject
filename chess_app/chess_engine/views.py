import chess 
import traceback

from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.template import loader

from chess_engine.models.game import Game
from chess_engine.models.playerBase import InitPlayer
from chess_engine.models.game_repository import GameRepository

GAME_REPO: GameRepository = GameRepository()
# Create your views here.
def index(request):
    return render(request, "chess_engine/index.html")

def createGame(request: HttpRequest):
    black = InitPlayer("manu", False)
    white = InitPlayer("random", True)
    game = Game(black, white)
    GAME_REPO.setCurrentGame(game)
    return render(request, "chess_engine/game.html", {
        "image": game.getBoardImage(),
        "white": game.players[True].name,
        "black": game.players[False].name,
        "current": game.players[game.board.turn],
        "history": game.getHistory(),
        "history": game.getHistory(),
        "draw": False,
        "draw_reason": "",
        "win": game.isCheckmate(),
        "error_message": "",
        })

def play(request: HttpRequest):
    move = request.POST.get("move")
    game = GAME_REPO.current_game
    results = {}
    if game.isCheckmate() or game.isDraw()[0]:
        is_draw = game.isDraw()
        results = {
        "image": game.getBoardImage(),
        "white": game.players[True].name,
        "black": game.players[False].name,
        "current": game.players[game.board.turn],
        "history": game.getHistory(),
        "draw": is_draw[0],
        "draw_reason": is_draw[1],
        "win": game.isCheckmate(),
        "error_message": "",
        }
        GAME_REPO.pushHistory()
    else:
        if game.players[game.currentColor()].is_ai:
            results = _ais(game)
        else:
            results = _player(move, game)

    if results["win"]:
        results["current"] = game.players[not game.board.turn]
    return render(request, "chess_engine/game.html", results)

def _player(move: str | None, game: Game):  
    error_message = ""
    is_draw = (False, "")
    if move is None:
        error_message = "no move present"
    else:
        try:
            uci_move = chess.Move.from_uci(move)
            if uci_move in game.legalMoves():
                game.play(uci_move)
                is_draw = game.isDraw()
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
        "draw": is_draw[0],
        "draw_reason": is_draw[1],
        "win": game.isCheckmate(),
        "error_message": error_message,
        }

def _ais(game: Game):
    error_message = ""
    game.play()
    is_draw = game.isDraw()
    return {
        "image": game.getBoardImage(),
        "white": game.players[True].name,
        "black": game.players[False].name,
        "current": game.players[game.board.turn],
        "history": game.getHistory(),
        "draw": is_draw[0],
        "draw_reason": is_draw[1],
        "win": game.isCheckmate(),
        "error_message": error_message,
        }