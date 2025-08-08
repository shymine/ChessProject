from typing import Optional
import chess
import chess.svg

from chess import Move
from chess_engine.models.concretePlayer import ConcretePlayer
from chess_engine.models.playerBase import InitPlayer, Player
from chess_engine.models.randomAI import RandomAI

AI: dict[str, Player] = {
    "random": RandomAI(InitPlayer("random", True))
}

class Game:
    def __init__(self, black: InitPlayer, white: InitPlayer) -> None:
        create = lambda p : self._createPlayer(p) if not p.is_ai else self._createAI(p)
        self.players = {
            chess.BLACK: create(black),
            chess.WHITE: create(white)
        }
        
        self.board = chess.Board()

    def _createPlayer(self, player: InitPlayer) -> Player :
        return ConcretePlayer(player)
    
    def _createAI(self, player: InitPlayer) -> Player:
        ai = AI[player.name]
        return ai

    def legalMoves(self) -> list[Move]:
        return list(self.board.legal_moves)
    
    def isCheckmate(self) -> bool:
        return self.board.is_checkmate()
    
    def isDraw(self) -> tuple[bool,str]:
        if self.board.is_insufficient_material():
            return (True, "Insufficient material")
        if self.board.is_stalemate():
            return (True, "Stalemate")
        if self.board.is_seventyfive_moves():
            return True, "75 moves without a pawn move or capture"
        if self.board.is_fivefold_repetition():
            return True, "5 fold repetition of the position"

        return (False, "")
    
    def currentColor(self) -> chess.Color:
        return self.board.turn
    
    def getHistory(self) -> list[Move] :
        return self.board.move_stack
    
    def getBoardImage(self) -> str:
        return chess.svg.board(
            self.board,
            lastmove= self.board.peek() if len(self.board.move_stack) > 0 else None
        )
    
    def play(self, move: Optional[Move] = None):
        if move is not None:
            self.board.push(move)
        else:
            print("color: ", self.currentColor(), "current player is ai: ", self.players[self.currentColor()].is_ai)
            ai_move = self.players[self.currentColor()].play(self.legalMoves())
            self.board.push(ai_move)
    
    def gameResultString(self):
        if self.board.is_game_over(claim_draw=True):
            return "1/2-1/2" if self.isDraw()[0] else ("1-0" if self.currentColor else "0-1")
        else:
            raise Exception("game not finished, impossible to generate result string")
            