from chess import Move
from chess_app.chess_engine.models.playerBase import InitPlayer, Player

class ConcretePlayer(Player):
    def __init__(self, player: InitPlayer) -> None:
        super().__init__(player)
    
    def play(self, moves: list[Move]) -> Move:
        if len(moves) != 1:
            raise Exception("move is not unique but it is a concrete player")
        return moves[0]