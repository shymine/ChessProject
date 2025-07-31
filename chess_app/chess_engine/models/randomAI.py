import random
from chess import Move
from chess_app.chess_engine.models.playerBase import InitPlayer, Player

class RandomAI(Player): 
    def __init__(self, player: InitPlayer) -> None:
        super().__init__(player)
    
    def play(self, moves: list[Move]) -> Move:
        if len(moves) == 0:
            raise Exception("there are no moves")
        if len(moves) == 1:
            return moves[0]
        
        move = random.randint(0, len(moves)-1)
        return moves[move]